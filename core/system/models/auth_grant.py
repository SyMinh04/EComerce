# from django.utils.timezone import now
# from django_cassandra_engine.models import DjangoCassandraModel
# from cassandra.cqlengine import columns
#
#
# class AuthGrant(DjangoCassandraModel):
#
#     CODE_CHALLENGE_PLAIN = "plain"
#     CODE_CHALLENGE_S256 = "S256"
#     CODE_CHALLENGE_METHODS = ((CODE_CHALLENGE_PLAIN, "plain"), (CODE_CHALLENGE_S256, "S256"))
#
#     user_id = columns.UUID(required=True)
#     user_type = columns.Text(max_length=20)
#     code = columns.Text(max_length=255)
#     application = columns.UUID(required=True)
#     expires = columns.DateTime(required=True)
#     redirect_uri = columns.Text(required=False)
#     scope = columns.Text(required=False)
#     code_challenge = columns.Text(max_length=128, required=False)
#     code_challenge_method = columns.Text(max_length=10, required=False)
#
#     nonce = columns.Text(max_length=255, required=False)
#     claims = columns.Text(required=False)
#
#     __table_name__ = 'auth_grants'
#
#     class Meta:
#         get_pk_field = 'uid'
#         db_table = 'auth_grants'
#
#     def is_expired(self):
#         """
#         Check token expiration with timezone awareness
#         """
#         if not self.expires:
#             return True
#
#         return now() >= self.expires
