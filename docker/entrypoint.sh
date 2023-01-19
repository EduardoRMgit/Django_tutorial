#!/bin/bash

# Extract private key from secrets
echo "${RENAPO_PRIVATE_KEY}" > renapo.pem
chmod 400 renapo.pem

# host name for stp
echo "192.168.66.211    prod.stpmex.com" >> /etc/hosts
echo "192.168.87.187    webs.curp.gob.mx" >> /etc/hosts

echo "|1|dGBySoddqblhiE3IFP0fIiEQBjg=|/2iqmk6+MmtFjyksiNjvJZ1F8Fw= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBC+aYJ8hwj6iX2fjVCbev5ziOKryfzMmQ1gdweKDIIuPOnS2/O/ztqxOzOI7AB2SSk2bBNVbg+4aNV6DIAaNalU=" >> /root/.ssh/known_hosts
echo "|1|osZXqV5SdNpvOBUK7WzOFkd4CtA=|dVBPJtWvxEOjlE+RY8Ub8WEDXOs= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBGhnMcYpnHXN1eLsdJYeVeQCEStBC5pCXoi7x6nufhqHL8LQOK5Ak5T8UBv/EhhOCdNLbkgx8VrOwQPv5+nXsfk=" >> /root/.ssh/known_hosts
echo "|1|IYcUeZ1Csj7fEIrBgDMPpab1o9w=|NhbPoscFTqndyORrBVTcIvQGzkw= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBGARF/qxGGWwCOMVfcdPXUM/1U52e98TaPqKCQf9ATSnKdQfixCyTjfWH0BC7K1bRwk/Tshjh1YWyi+DttAcsac=" >> /root/.ssh/known_hosts
echo "|1|XwewPI2/IqDBYzqmiVvIT85s0WY=|KSahCjWXy6lzAi+G0jkX7Tk+qrI= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBCMcXR9ZLmY4NX3JMIOSVMIcUxnU8bEy8CGzz/qx1xJekkMdsUTJgtgJSICHO/06gojVLSQnWj7+ziAA4Feb0gU=" >> /root/.ssh/known_hosts
echo "|1|lyRk8O8I9dkbEx6LPOlPIxbZ6Ys=|Ukp/nnqO4n6/X2NxFPDCj0OYdP4= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBIwTGci9IQ2W1K8vUQT106RE+8LqCVl15rVSSnJTDkuM9Jkqawa8X1y3vtsLoVaqXe3UzED14KNu+9w1a+vzElI=" >> /root/.ssh/known_hosts
chmod 400 neto.pem
# send current ip to scotia proxy
if [[ $SITE == 'stage' ]] ; then
    cat /etc/hosts | grep cactus-$SITE > my_ip 
    # scotia
    scp -i neto.pem my_ip ubuntu@192.168.93.229:stage_ip
    # stp
    scp -i neto.pem my_ip ubuntu@192.168.66.211:stage_ip_${HASH}_$(hostname)
    # renapo
    scp -i renapo.pem my_ip ubuntu@192.168.87.187:stage_ip_${HASH}_$(hostname)
fi;

if [[ $SITE == 'test' ]] ; then
    cat /etc/hosts | grep cactus-$SITE > my_ip
    # scotia
    scp -i neto.pem my_ip ubuntu@192.168.93.229:test_ip
    # stp
    scp -i neto.pem my_ip ubuntu@192.168.66.211:test_ip_${HASH}_$(hostname)
    # renapo
    scp -i renapo.pem my_ip ubuntu@192.168.87.187:test_ip_${HASH}_$(hostname)
fi;

if [[ $SITE == 'prod' ]] ; then
    # Extract private key from secrets
    echo "${STP_PK}" > llavePrivada.pem
    unset STP_PK

    cat /etc/hosts | grep cactus-$SITE > my_ip
    # scotia
    scp -i neto.pem my_ip ubuntu@192.168.93.229:prod_ip
    # stp
    scp -i neto.pem my_ip ubuntu@192.168.66.211:prod_ip_${HASH}_$(hostname)
    # renapo
    scp -i renapo.pem my_ip ubuntu@192.168.87.187:prod_ip_${HASH}_$(hostname)
fi;

chmod +w renapo.pem
rm renapo.pem
unset RENAPO_PRIVATE_KEY

# Standard
gunicorn --bind 0.0.0.0:8000 -t 2400 cactus.wsgi --log-level debug
