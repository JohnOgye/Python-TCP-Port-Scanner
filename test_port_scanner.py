import argparse
import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import port_scanner


class TestPortScanner(unittest.TestCase):

    @patch("port_scanner.socket.gethostbyname")
    def test_resolve_target_success(self, mock_gethostbyname):
        mock_gethostbyname.return_value = "127.0.0.1"

        result = port_scanner.resolve_target("localhost")

        self.assertEqual(result, "127.0.0.1")

    @patch("port_scanner.socket.gethostbyname")
    def test_resolve_target_failure(self, mock_gethostbyname):
        mock_gethostbyname.side_effect = socket.gaierror

        result = port_scanner.resolve_target("invalid-host")

        self.assertIsNone(result)

    @patch("port_scanner.socket.getservbyport")
    def test_get_service_name_known(self, mock_getservbyport):
        mock_getservbyport.return_value = "http"

        result = port_scanner.get_service_name(80)

        self.assertEqual(result, "http")

    @patch("port_scanner.socket.getservbyport")
    def test_get_service_name_unknown(self, mock_getservbyport):
        mock_getservbyport.side_effect = OSError

        result = port_scanner.get_service_name(5000)

        self.assertEqual(result, "Unknown")

    @patch("port_scanner.socket.socket")
    def test_scan_port_open(self, mock_socket):
        mock_sock = MagicMock()

        mock_socket.return_value.__enter__.return_value = mock_sock
        mock_sock.connect_ex.return_value = 0

        with patch(
            "port_scanner.get_service_name",
            return_value="Unknown"
        ):
            is_open, service = port_scanner.scan_port(
                "127.0.0.1",
                5000
            )

        self.assertTrue(is_open)
        self.assertEqual(service, "Unknown")

    @patch("port_scanner.socket.socket")
    def test_scan_port_closed(self, mock_socket):
        mock_sock = MagicMock()

        mock_socket.return_value.__enter__.return_value = mock_sock
        mock_sock.connect_ex.return_value = 1

        is_open, service = port_scanner.scan_port(
            "127.0.0.1",
            5000
        )

        self.assertFalse(is_open)
        self.assertIsNone(service)

    @patch("port_scanner.scan_port")
    def test_scan_ports_finds_open_ports(self, mock_scan_port):
        def fake_scan(target_ip, port):
            if port == 5000:
                return True, "Unknown"

            return False, None

        mock_scan_port.side_effect = fake_scan

        result = port_scanner.scan_ports(
            "127.0.0.1",
            4998,
            5002,
            max_workers=3
        )

        self.assertEqual(
            result,
            [(5000, "Unknown")]
        )

    @patch("port_scanner.scan_port")
    def test_scan_ports_returns_sorted_results(self, mock_scan_port):
        def fake_scan(target_ip, port):
            if port in (4999, 5001):
                return True, "Unknown"

            return False, None

        mock_scan_port.side_effect = fake_scan

        result = port_scanner.scan_ports(
            "127.0.0.1",
            4998,
            5002,
            max_workers=3
        )

        self.assertEqual(
            result,
            [
                (4999, "Unknown"),
                (5001, "Unknown")
            ]
        )

    def test_save_results(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = Path(temp_dir) / "results.txt"

            open_ports = [
                (5000, "Unknown")
            ]

            port_scanner.save_results(
                filename,
                "127.0.0.1",
                "127.0.0.1",
                4995,
                5005,
                open_ports,
                1.25
            )

            contents = filename.read_text(
                encoding="utf-8"
            )

            self.assertIn(
                "Target: 127.0.0.1",
                contents
            )

            self.assertIn(
                "Open ports found: 1",
                contents
            )

            self.assertIn(
                "Port 5000",
                contents
            )
    def test_port_number_valid(self):
        result = port_scanner.port_number("443")

        self.assertEqual(result, 443)


    def test_port_number_invalid(self):
        with self.assertRaises(
            argparse.ArgumentTypeError
        ):
            port_scanner.port_number("0")


    def test_positive_timeout_valid(self):
        result = port_scanner.positive_timeout("1.5")

        self.assertEqual(result, 1.5)


    def test_worker_count_valid(self):
        result = port_scanner.worker_count("25")

        self.assertEqual(result, 25)


    def test_argument_parser_defaults(self):
        parser = port_scanner.build_parser()

        args = parser.parse_args(
            [
                "127.0.0.1",
                "-s",
                "1",
                "-e",
                "100"
            ]
        )

        self.assertEqual(
            args.target,
            "127.0.0.1"
        )
        self.assertEqual(
            args.start_port,
            1
        )
        self.assertEqual(
            args.end_port,
            100
        )
        self.assertEqual(
            args.timeout,
            port_scanner.DEFAULT_TIMEOUT
        )
        self.assertEqual(
            args.workers,
            port_scanner.MAX_WORKERS
        )
        self.assertEqual(
            args.output,
            port_scanner.RESULTS_FILE
        )


    def test_argument_parser_custom_options(self):
        parser = port_scanner.build_parser()

        args = parser.parse_args(
            [
                "127.0.0.1",
                "--start-port",
                "4995",
                "--end-port",
                "5005",
                "--timeout",
                "1.0",
                "--workers",
                "25",
                "--output",
                "custom_results.txt"
            ]
        )

        self.assertEqual(
            args.start_port,
            4995
        )
        self.assertEqual(
            args.end_port,
            5005
        )
        self.assertEqual(
            args.timeout,
            1.0
        )
        self.assertEqual(
            args.workers,
            25
        )
        self.assertEqual(
            args.output,
            "custom_results.txt"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)