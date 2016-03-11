# -*- coding: utf-8 -*-
from django.db import models

RADOP_CHECK_TYPES = (
    ('=', '='),
    (':=', ':='),
    ('==', '=='),
    ('+=', '+='),
    ('!=', '!='),
    ('>', '>'),
    ('>=', '>='),
    ('<', '<'),
    ('<=', '<='),
    ('=~', '=~'),
    ('!~', '!~'),
    ('=*', '=*'),
    ('!*', '!*'),
)
RADOP_REPLY_TYPES = (
    ('=', '='),
    (':=', ':='),
    ('+=', '+='),
)

class Realmgroup(models.Model):
    class Meta:
        db_table = 'realmgroup'

    realmname = models.CharField(max_length=30)
    groupname = models.CharField(max_length=30)
    def __str__(self):
        return str(self.realmname)


class Realms(models.Model):
    class Meta:
        db_table = 'realms'
        verbose_name_plural = "realms"

    realmname = models.CharField(max_length=64)
    nas = models.CharField(max_length=128)
    authport = models.IntegerField()
    options = models.CharField(max_length=128)
    def __str__(self):
        return str(self.realmname)


class Attributelist(models.Model):
    class Meta:
        db_table = 'attributelist'

    attribute = models.CharField(max_length=60)
    enabled = models.BooleanField()
    checkitem = models.BooleanField()
    def __str__(self):
        return str(self.attribute)


class Nas(models.Model):
    class Meta:
        db_table = 'nas'
        verbose_name_plural = "nas"

    NAS_TYPES = (
        ('cisco', 'cisco'),
        ('computone', 'computone'),
        ('livingston', 'livingston'),
        ('juniper', 'juniper'),
        ('max40xx', 'max40xx'),
        ('mikrotik', 'mikrotik'),
        ('multitech', 'multitech'),
        ('netserver', 'netserver'),
        ('pathras', 'pathras'),
        ('patton', 'patton'),
        ('portslave', 'portslave'),
        ('tc', 'tc'),
        ('usrhiper', 'usrhiper'),
        ('other', 'other'),
    )

    vhost = models.CharField(max_length=128, unique=True, help_text='NAS Name (or IP address)')
    nasname = models.CharField(max_length=128, unique=True, help_text='NAS Name (or IP address)')
    shortname = models.CharField(max_length=32)
    type = models.CharField(max_length=30, choices=NAS_TYPES)
    secret = models.CharField(max_length=60, help_text='Shared Secret')
    coasecret = models.CharField(max_length=60, help_text='CoA Secret', blank=True, null=True)
    ports = models.IntegerField(blank=True, null=True)
    naslocation = models.CharField(max_length=32, blank=True, null=True)
    community = models.CharField(max_length=50, blank=True, null=True)
    snmp = models.CharField(max_length=10, blank=True, null=True)
    def __str__(self):
        return str(self.nasname)


class Radpostauth(models.Model):
    class Meta:
        db_table = 'radpostauth'
        verbose_name_plural = "radpostauth"

    username = models.CharField(max_length=64)
    password = models.CharField(db_column='pass', max_length=64) # Field renamed because it was a Python reserved word.
    reply = models.CharField(max_length=32)
    authdate = models.DateTimeField()
    calledstationid = models.CharField(max_length=64)
    callingstationid = models.CharField(max_length=50)
    def __str__(self):
        return str(self.username)


class Radreply(models.Model):
    class Meta:
        db_table = 'radreply'
        verbose_name_plural = "radreply"

    username = models.CharField(max_length=30)
    attribute = models.CharField(max_length=30)
    op = models.CharField(max_length=2, choices=RADOP_REPLY_TYPES)
    value = models.CharField(max_length=40)
    calledstationid = models.CharField(max_length=64)
    custid = models.IntegerField()
    def __str__(self):
        return str(self.username)


class Radusergroup(models.Model):
    class Meta:
        db_table = 'radusergroup'

    username = models.CharField(max_length=30)
    groupname = models.CharField(max_length=30)
    calledstationid = models.CharField(max_length=64)
    def __str__(self):
        return str(self.username)


class Radcheck(models.Model):
    class Meta:
        db_table = 'radcheck'
        verbose_name_plural = "radcheck"

    username = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2, choices=RADOP_CHECK_TYPES)
    value = models.CharField(max_length=253)
    def __str__(self):
        return str(self.username)


class Radgroupcheck(models.Model):
    class Meta:
        db_table = 'radgroupcheck'
        verbose_name_plural = "radgroupcheck"

    groupname = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2, choices=RADOP_CHECK_TYPES)
    value = models.CharField(max_length=253)


class Radgroupreply(models.Model):
    class Meta:
        db_table = 'radgroupreply'
        verbose_name_plural = "radgroupreply"

    groupname = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2, choices=RADOP_REPLY_TYPES)
    value = models.CharField(max_length=253)
    def __str__(self):
        return str(self.groupname)


class Radippool(models.Model):
    class Meta:
        db_table = 'radippool'
        verbose_name_plural = "radippool"

    pool_name = models.CharField(max_length=64,help_text='The IP Pool name')
    framedipaddress = models.IPAddressField(help_text='The users IP address')
    nasipaddress = models.CharField(max_length=16)
    callingstationid = models.TextField('Calling-Station-Id', help_text='The MAC Address or CLI of the user')
    expiry_time = models.DateTimeField(help_text='The IP Lease expiry time')
    username = models.CharField(max_length=64)
    groupname = models.CharField(max_length=30)
    pool_key = models.CharField(max_length=30)
    fixed = models.BooleanField()
    def __str__(self):
        return str(self.framedipaddress)


class Radacct(models.Model):
    class Meta:
        db_table = 'radacct'
        verbose_name_plural = "radacct"

    radacctid = models.AutoField(primary_key=True)
    acctsessionid = models.CharField(max_length=32)
    acctuniqueid = models.CharField(max_length=32)
    username = models.CharField(max_length=253, null=True)
    realm = models.CharField(max_length=64, null=True)
    nasipaddress = models.IPAddressField()
    nasportid = models.CharField(max_length=15, null=True)
    nasporttype = models.CharField(max_length=32, null=True)
    acctstarttime = models.DateTimeField(null=True)
    acctstoptime = models.DateTimeField(null=True)
    acctsessiontime = models.BigIntegerField(null=True)
    acctauthentic = models.CharField(max_length=32, null=True)
    acctinputoctets = models.BigIntegerField(null=True)
    acctoutputoctets = models.BigIntegerField(null=True)
    calledstationid = models.CharField(max_length=50, null=True)
    callingstationid = models.CharField(max_length=50, null=True)
    framedipaddress = models.IPAddressField(null=True)
    connectinfo_start = models.CharField(max_length=50, null=True)
    connectinfo_stop = models.CharField(max_length=50, null=True)
    acctterminatecause = models.CharField(max_length=32, null=True)
    servicetype = models.CharField(max_length=32, null=True)
    framedprotocol = models.CharField(max_length=32, null=True)
    acctstartdelay = models.IntegerField(null=True)
    acctstopdelay = models.IntegerField(null=True)
    xascendsessionsvrkey = models.CharField(max_length=10, null=True)
    def __str__(self):
        return str(self.acctuniqueid)

