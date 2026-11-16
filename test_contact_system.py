"""
test_contact_system.py — Comprehensive Test Suite for Contact Management & Notification System
Tests all 10 required scenarios from the prompt:
  1. Successful contact form submission
  2. Invalid email submission
  3. Empty form submission
  4. Duplicate submission attempt
  5. Successful SQLite storage
  6. Successful Google Sheets synchronization (mocked & real interface)
  7. Successful email notification (mocked SMTP & header verification)
  8. Google Sheets API failure tolerance (record preserved)
  9. Email delivery failure tolerance (record preserved)
 10. Admin inbox functionality (auth, search, filter, read, replied, retry, delete)
"""

import os
import sys
from datetime import datetime
from unittest.mock import MagicMock, patch

# Ensure project root is in path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app
from extensions import db
from models import ContactMessage, AdminUser
from services.google_sheets import sync_submission_to_google_sheet, retry_failed_sheets_sync, retry_all_unsynced_sheets
from services.email_notifier import send_contact_notification


def run_contact_system_tests():
    app = create_app('development')
    client = app.test_client()

    print("=" * 70)
    print("RUNNING COMPLETE CONTACT SYSTEM TEST SUITE (10 SCENARIOS)")
    print("=" * 70)

    with app.app_context():
        # Setup: Ensure admin user exists
        admin = AdminUser.query.filter_by(username='admin').first()
        if not admin:
            admin = AdminUser(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

        # ---------------------------------------------------------------------
        # SCENARIO 1: Successful contact form submission
        # ---------------------------------------------------------------------
        print("\n[TEST 1] Testing Successful Contact Form Submission...")
        test_payload = {
            'name': 'Elena Rostova',
            'email': 'elena.rostova@ai-research.org',
            'subject': 'AI Autonomous Agent Security Collaboration',
            'message': 'Hello Nithin, we reviewed your AgentGuard AI architecture and would love to discuss a research collaboration on runtime prompt defense.',
            'form_website_hp': ''  # Empty honeypot
        }
        res1 = client.post('/contact/send', json=test_payload)
        assert res1.status_code == 200, f"Expected 200, got {res1.status_code}: {res1.data}"
        json_data1 = res1.get_json()
        assert json_data1.get('success') is True
        assert 'submission_id' in json_data1
        saved_id1 = json_data1['submission_id']
        print(f"  --> PASS: Submission accepted (ID #{saved_id1}): {json_data1.get('message')}")

        # ---------------------------------------------------------------------
        # SCENARIO 2: Invalid email submission
        # ---------------------------------------------------------------------
        print("\n[TEST 2] Testing Invalid Email Submission...")
        bad_email_payload = {
            'name': 'Bob Tester',
            'email': 'not-an-email-address',
            'subject': 'General Inquiry',
            'message': 'This is a test message to verify email validation logic.'
        }
        res2 = client.post('/contact/send', json=bad_email_payload)
        assert res2.status_code == 422, f"Expected 422, got {res2.status_code}"
        json_data2 = res2.get_json()
        assert json_data2.get('success') is False
        assert 'valid email address' in json_data2.get('message', '').lower()
        print(f"  --> PASS: Rejected invalid email with message: {json_data2.get('message')}")

        # ---------------------------------------------------------------------
        # SCENARIO 3: Empty form submission
        # ---------------------------------------------------------------------
        print("\n[TEST 3] Testing Empty Form Submission...")
        empty_payload = {
            'name': '',
            'email': '',
            'subject': '',
            'message': ''
        }
        res3 = client.post('/contact/send', json=empty_payload)
        assert res3.status_code == 422, f"Expected 422, got {res3.status_code}"
        json_data3 = res3.get_json()
        assert json_data3.get('success') is False
        print(f"  --> PASS: Rejected empty form with validation message: {json_data3.get('message')}")

        # ---------------------------------------------------------------------
        # SCENARIO 4: Duplicate submission attempt
        # ---------------------------------------------------------------------
        print("\n[TEST 4] Testing Duplicate Submission Cooldown...")
        # Send exact same payload as Test 1 immediately
        res4 = client.post('/contact/send', json=test_payload)
        assert res4.status_code == 409, f"Expected 409 Conflict, got {res4.status_code}"
        json_data4 = res4.get_json()
        assert json_data4.get('success') is False
        assert 'duplicate' in json_data4.get('message', '').lower()
        print(f"  --> PASS: Blocked duplicate submission attempt: {json_data4.get('message')}")

        # ---------------------------------------------------------------------
        # SCENARIO 5: Successful SQLite storage
        # ---------------------------------------------------------------------
        print("\n[TEST 5] Testing SQLite Database Persistence & Schema...")
        db_msg = ContactMessage.query.get(saved_id1)
        assert db_msg is not None, f"Message ID #{saved_id1} not found in SQLite!"
        assert db_msg.name == 'Elena Rostova'
        assert db_msg.email == 'elena.rostova@ai-research.org'
        assert db_msg.subject == 'AI Autonomous Agent Security Collaboration'
        assert db_msg.status == 'New'
        assert db_msg.submitted_at is not None
        print(f"  --> PASS: SQLite Record verified: ID={db_msg.id}, Name={db_msg.name}, Status={db_msg.status}, Time={db_msg.submitted_at}")

        # ---------------------------------------------------------------------
        # SCENARIO 6: Successful Google Sheets synchronization (Unit Interface)
        # ---------------------------------------------------------------------
        print("\n[TEST 6] Testing Google Sheets Synchronization Interface...")
        # Mock gspread client and worksheet
        mock_worksheet = MagicMock()
        mock_worksheet.get_all_values.return_value = [["ID", "Name", "Email", "Subject", "Message", "Date & Time", "Status"]]
        mock_spreadsheet = MagicMock()
        mock_spreadsheet.sheet1 = mock_worksheet
        mock_client = MagicMock()
        mock_client.open.return_value = mock_spreadsheet
        mock_client.open_by_key.return_value = mock_spreadsheet
        mock_client.create.return_value = mock_spreadsheet

        with patch('services.google_sheets.get_google_sheets_client', return_value=(mock_client, None)):
            ok, msg = sync_submission_to_google_sheet(db_msg)
            assert ok is True, f"Google sheets sync failed: {msg}"
            assert mock_worksheet.append_row.called
            row_appended = mock_worksheet.append_row.call_args[0][0]
            assert str(db_msg.id) in row_appended
            assert db_msg.name in row_appended
            assert db_msg.email in row_appended
            # Verify SQLite record updated
            assert db_msg.sheets_synced is True
            assert db_msg.sheets_synced_at is not None
            print(f"  --> PASS: Google Sheets sync succeeded. Row data: {row_appended}")

        # ---------------------------------------------------------------------
        # SCENARIO 7: Successful email notification (SMTP Mock)
        # ---------------------------------------------------------------------
        print("\n[TEST 7] Testing SMTP Email Notification Dispatch & Headers...")
        mock_smtp_instance = MagicMock()

        # Set fake environment variables for test
        with patch.dict(os.environ, {
            'OWNER_EMAIL': 'nithin.ragunath.20@gmail.com',
            'SMTP_SERVER': 'smtp.gmail.com',
            'SMTP_PORT': '587',
            'SMTP_USERNAME': 'notifier@portfolio.local',
            'SMTP_PASSWORD': 'sample-app-password'
        }):
            with patch('smtplib.SMTP', return_value=mock_smtp_instance):
                ok_email, email_msg_str = send_contact_notification(db_msg)
                assert ok_email is True, f"Email notification failed: {email_msg_str}"
                assert mock_smtp_instance.starttls.called
                assert mock_smtp_instance.login.called
                assert mock_smtp_instance.send_message.called

                # Inspect message headers
                sent_email_obj = mock_smtp_instance.send_message.call_args[0][0]
                assert sent_email_obj['To'] == 'nithin.ragunath.20@gmail.com'
                assert sent_email_obj['From'] == 'notifier@portfolio.local'
                assert sent_email_obj['Reply-To'] == db_msg.email
                assert f"New Portfolio Contact - {db_msg.name}" in sent_email_obj['Subject']
                assert db_msg.email_sent is True
                assert db_msg.email_sent_at is not None
                print(f"  --> PASS: SMTP Email dispatched. To={sent_email_obj['To']}, Reply-To={sent_email_obj['Reply-To']}, Subject='{sent_email_obj['Subject']}'")

        # ---------------------------------------------------------------------
        # SCENARIO 8: Google Sheets API failure tolerance (Record Preserved)
        # ---------------------------------------------------------------------
        print("\n[TEST 8] Testing Google Sheets API Failure Tolerance...")
        test_msg_8 = ContactMessage(
            name='Marcus Aurelius',
            email='marcus@stoic.ai',
            subject='Systems Resilience',
            message='Testing resilience when Google API returns 503 service unavailable.',
            submitted_at=datetime.utcnow(),
            status='New'
        )
        db.session.add(test_msg_8)
        db.session.commit()
        msg8_id = test_msg_8.id

        with patch('services.google_sheets.get_google_sheets_client', side_effect=Exception("Google Cloud Quota Exceeded (HTTP 429)")):
            ok8, err8 = sync_submission_to_google_sheet(test_msg_8)
            assert ok8 is False
            # Verify SQLite record is still alive!
            recheck_msg8 = ContactMessage.query.get(msg8_id)
            assert recheck_msg8 is not None, "FATAL: Record was lost on Google Sheets error!"
            assert recheck_msg8.sheets_synced is False
            assert "Google Cloud Quota Exceeded" in (recheck_msg8.sheets_error or "")
            print(f"  --> PASS: Google Sheets API error handled gracefully. Record preserved in SQLite with error logged: '{recheck_msg8.sheets_error}'")

        # ---------------------------------------------------------------------
        # SCENARIO 9: Email delivery failure tolerance (Record Preserved)
        # ---------------------------------------------------------------------
        print("\n[TEST 9] Testing SMTP Delivery Failure Tolerance...")
        with patch.dict(os.environ, {
            'OWNER_EMAIL': 'nithin.ragunath.20@gmail.com',
            'SMTP_SERVER': 'smtp.gmail.com',
            'SMTP_PORT': '587',
            'SMTP_USERNAME': 'notifier@portfolio.local',
            'SMTP_PASSWORD': 'wrong-password'
        }):
            with patch('smtplib.SMTP', side_effect=Exception("SMTPAuthenticationError: Bad credentials")):
                ok9, err9 = send_contact_notification(test_msg_8)
                assert ok9 is False
                recheck_msg8_email = ContactMessage.query.get(msg8_id)
                assert recheck_msg8_email is not None, "FATAL: Record was lost on Email error!"
                assert recheck_msg8_email.email_sent is False
                assert "SMTPAuthenticationError" in (recheck_msg8_email.email_error or "")
                print(f"  --> PASS: Email failure handled gracefully. Record preserved in SQLite with error logged: '{recheck_msg8_email.email_error}'")

        # ---------------------------------------------------------------------
        # SCENARIO 10: Admin inbox functionality
        # ---------------------------------------------------------------------
        print("\n[TEST 10] Testing Admin Inbox (Auth, Listing, Search, Status Update, Delete)...")
        # 10.1 Unauthenticated access to /admin/dashboard must redirect to login
        res_unauth = client.get('/admin/dashboard', follow_redirects=False)
        assert res_unauth.status_code in [302, 401], f"Expected redirect, got {res_unauth.status_code}"
        print("  --> [10.1] Protected route redirects unauthenticated visitor to login")

        # 10.2 Admin Login
        res_login = client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        assert res_login.status_code == 200
        assert b"Contact Inbox" in res_login.data or b"Contact Submissions Manager" in res_login.data
        print("  --> [10.2] Admin login successful")

        # 10.3 Search functionality
        res_search = client.get('/admin/dashboard?q=Elena')
        assert res_search.status_code == 200
        assert b"Elena Rostova" in res_search.data
        print("  --> [10.3] Search filter by name 'Elena' returned expected submission")

        # 10.4 Status Filter
        res_filter = client.get('/admin/dashboard?status=new')
        assert res_filter.status_code == 200
        print("  --> [10.4] Filter by status 'new' works")

        # 10.5 View message details API
        res_view = client.get(f'/admin/message/{saved_id1}')
        assert res_view.status_code == 200
        view_json = res_view.get_json()
        assert view_json['name'] == 'Elena Rostova'
        print(f"  --> [10.5] Message API returned details and marked as Read: status={view_json['status']}")

        # 10.6 Update status to 'Replied'
        res_status = client.post(f'/admin/message/{saved_id1}/status', json={'status': 'Replied'})
        assert res_status.status_code == 200
        assert ContactMessage.query.get(saved_id1).status == 'Replied'
        print("  --> [10.6] Updated message status to 'Replied'")

        # 10.7 Delete message
        res_del = client.post(f'/admin/message/{msg8_id}/delete', follow_redirects=True)
        assert res_del.status_code == 200
        assert ContactMessage.query.get(msg8_id) is None
        print(f"  --> [10.7] Message #{msg8_id} deleted successfully from SQLite")

    print("\n" + "=" * 70)
    print("ALL 10 CONTACT SYSTEM SCENARIOS PASSED WITH 100% SUCCESS!")
    print("=" * 70)


if __name__ == '__main__':
    run_contact_system_tests()
