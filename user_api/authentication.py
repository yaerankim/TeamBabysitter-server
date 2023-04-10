import os

import firebase_admin
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from firebase_admin import auth
from firebase_admin import credentials
from rest_framework import authentication
from rest_framework import exceptions

from .exceptions import FirebaseError
from .exceptions import InvalidAuthToken
from .exceptions import NoAuthToken

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": os.environ.get('fir-emailaccount-fa39e'),
  "private_key_id": os.environ.get('afcaa8070957de76f809c344de1fc9995de4c12d'),
  "private_key": os.environ.get('-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDIZRV+pvavetr+\nv4eSbme0yWSshKXsg2uokcsTHzR9aEbQy6Z1BIV2KgtGV9IhUOXFQyNyNbLPsKJx\nUXPLicueoIbcGdNogqr7HpPNEDuXUCkY3sZdh3AGWVydivyBYinDscwUbWqAtMsb\nHSX+Fd8Ma2eTYjP4nhoGK4GnON+z1VGmGBU1iC1PJLvUZn4Xr3kZYwpEWql5FR8/\njWVlHSJde6V4yhU2WGYmgl9lRBQM3nHc5pO0FphcRYFssVcAn+T1BhRuyTHzEVyX\nlY8nmwGOSAWrdsKoSzHUMx8um2PWIOyWB9+YiYeT4qjRPJvqfBDlGC4odlEg8P96\nixQq95QdAgMBAAECggEAL9jy6Oq0u/F5mJnipPP3jxMHFqoVdANtETK+ajJpNghP\n4Eq/0/DgbPZc+s69PXczZYZCUGLB7xUdtDDelRqxo45wpN0FvU51xL/oSm41zEs3\nhNisRGiyNtHfaz5kTABEOJWbRMVbSJ/iXvb2u1Q9jZmXgXlRL2uQiyiYLHVH9Ifu\nY0VP4vWOeKzPjL/YU/1mVeTXU+J0cIlXgUp+vxmfQ9BXhga8/Jn+pKMC0il4e1gG\nKFYG/rYcKCuy47Z0MT3yu0KkFiIuyGWp+rvBxW3vQcErnJvPTWbQ5sq8m7eN1Vxx\nO2qAvt+o9AVrb9L28BLpPhDd7vUB4RMENxe/twVzgQKBgQDowE3g74XnjxWrgaoF\nM/OG1gkTHFbs/vfSak17B6ec77tjzPv5Bow7MjcXJ3klRNkG8Vk7F17sT5WOIoTB\nP7rVZxKaNckPDgpK1Wo9mkLj24iwixeNkP8UJnNmnUycQ480peA2YLdtkHid49Zd\nOtvXaWj3HLchJRncKC96GJllvwKBgQDcaWTaF9mtLIEOVaAehSVEI8Ht2hy6mIPH\nKYDUvm9EB+7tBNTd1WBmqFtjpDN2Sydr9hW7vb8V1ATXSot5W48jjywHKsNT7qPS\n7g0DAU7gtqqyWVBaojDruNBq+0B9BZMuYuAAffckr2qTN8PYBuRkIkJjjDjkPGoo\n6j5vbNoVIwKBgE+kJcHXE9GlMzwJVT0MhsLXkCla5B+aKwBz4Wk8uEzJ9yvyIzIV\n3HwQ9arVle17vmtSwD6pA5EGtlz5UMWzYeHNsB7WUqL1Ie5zUjQcCdFf+Ei4f2mw\neKfTdF9jaah6sZDJRYw10e4KpksYf+xMzJbL+d+8kqkjwdKEaaJ0smCPAoGBAMDt\ni/aOy92WR/zZHEe6ucz0E6rzsRPvreFlxbvyWQhOfWeARCdMv438LcqBDv6rd/07\nMPjddOZRaE9ek8kNSLSSfLJlTwYnq8RU1JTdz0JJAg8MuJYsw++BHQWXmXIVsCf5\nKiOkHvFAjmQAeu+b0MyJZF0ofx/gdfgMWcxElnvLAoGBALkrFDG6iKNEDLvCFi+a\nQ0OP5/jovfY5DIrXJZTHXAqudwiQTHm4N3VhC220c9gmBEeyajjQLQYHoUxY835E\nr/smBY51rmzRhWa30Kj+ovoJT71Qr7T7sFuIw3clXZ7BNVdoIITVIHeghx6z+r7C\nCTBH0G6asNL1Q2BA24mNJPgD\n-----END PRIVATE KEY-----\n').replace('\\n', '\n'),
  "client_email": os.environ.get('firebase-adminsdk-87mv2@fir-emailaccount-fa39e.iam.gserviceaccount.com'),
  "client_id": os.environ.get('117699178119405457291'),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.environ.get('https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-87mv2%40fir-emailaccount-fa39e.iam.gserviceaccount.com')
})

default_app = firebase_admin.initialize_app(cred)

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken("Invalid auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()

        user, created = User.objects.get_or_create(username=uid)
        user.profile.last_activity = timezone.localtime()

        return (user, None)