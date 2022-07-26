import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from Encryptor.hasher_tools import hasher
from Encryptor.encryptor import SymmetricEncryptor

from django.db import transaction

class UserManager(BaseUserManager):

    @transaction.atomic
    def create_user(self, username, security_passphrase,kc_pp,kc_apikey,kc_secret,password=None):
        """
        A manager to create user to suit our needs
        takes the secrets provided by user , encrypts them with a generated hash and saves them
        to the database
        :param username:
        :param security_passphrase:
            The whole idea of this field is to provide much secure app . we take the pass phrase,
            hash it with custom hasher in Encryptor/hasher_tools and save the hash in the database.

            Each time user calls a request , we ask him/her to provide the security pass phrase,
            we take it and check it if it's correct . then we create a kdf(key driven function) by
            concatenating hashed pass phrase with hashed uuid and hashing it.

            with this kdf , we encrypt the user secrets . so each user will have his/her own individual
            kdf to decrypt back the encrypted secrets and not having only one key in .env file to decrypt
            every single users secrets .
        :param kc_pp:
            Kucoin pass phrase provided by kucoin for user
        :param kc_apikey:
            Kucoin api key provided by kucoin for user
        :param kc_secret:
            Kucoin secret phrase provided by kucoin for user
        :param password:
            User Password for logging i
        :return:
        """

        if not username:
            raise exceptions.ValidationError({'Username': ['Username is Required.']})
        try:
            user = self.model(
                username=username,
            )
            user.save(using=self._db)
            user.set_password(password)
            user.is_active = True
            ## we hash the provided fields , to get an encryption key (kdf)
            hashed_p_phrase = hasher(security_passphrase)
            hashed_uuid = hasher(str(user.id))
            encrypt_key = hasher(hashed_p_phrase + hashed_uuid)
            ## instantiating SymmetricEncryptor with the generated kdf for this specific user
            sym_enc = SymmetricEncryptor(encrypt_key)

        except NotImplementedError or TypeError as e:
            """
            :raise NotImplementedError if salt is not provided in .env file
            """
            print(e)
            raise exceptions.ValidationError('Something went wrong try again!')

        # Saving hashed pass phrase in db
        user.security_passphrase = hashed_p_phrase.decode("utf-8")
        # Saving Encrypted secrets in the db
        user.kc_pp = sym_enc.encrypt(kc_pp)
        user.kc_apikey = sym_enc.encrypt(kc_apikey)
        user.kc_secret = sym_enc.encrypt(kc_secret)
        user.save()
        return user

    def create_superuser(self, username, password=None):
        if not password:
            raise exceptions.ValidationError({'Password': ['Password is Required.']})

        admin = self.model(
            username=username,

        )

        admin.set_password(password)
        admin.auto_update_orders = False
        admin.is_active = True
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_admin = True
        admin.save(using=self._db)
        return admin


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(verbose_name='Username', max_length=65, unique=True, blank=False, null=False)
    name = models.CharField(verbose_name='Name', max_length=75, null=True, blank=True)

    #This field is a second security layer (each api call needs pass phrase to be provided)
    security_passphrase = models.CharField(max_length=255,null=True,blank=True,verbose_name='Security Pass phrase')

    kc_pp = models.CharField(max_length=255,null=True,blank=True,verbose_name='Kucoin Pass Phrase')
    kc_apikey = models.CharField(max_length=255,null=True,blank=True,verbose_name='Kucoin Api Key')
    kc_secret = models.CharField(max_length=255,null=True,blank=True,verbose_name='Kucoin Secret')
    auto_update_orders = models.BooleanField(default=True,verbose_name='Enable Auto Update Orders')
    last_login = models.DateTimeField(verbose_name='Update at', auto_now=True)
    date_joined = models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self) -> str:
        return self.username


    def decrypted_secrets_collection(self,kdf) -> dict:
        """
        Decrypts the stored kucoin secrets of the user

        :return: a dictionary containing kucoin pass_phrase , secret and api key in raw format
        """

        sym_enc = SymmetricEncryptor(kdf)
        return {
            'kc_pp':sym_enc.decrypt(self.kc_pp),
            'kc_secret':sym_enc.decrypt(self.kc_secret),
            'kc_apikey':sym_enc.decrypt(self.kc_apikey),
        }

    @property
    def tokens(self) -> dict:
        """
        Creates refresh and access token for user (simple jwt package)
        :return: a dictionary containing refresh and access token
        """
        token = RefreshToken.for_user(self)
        data = {
            'refresh': str(token),
            'access': str(token.access_token)
        }
        return data

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('date_joined',)