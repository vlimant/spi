import os
import string
fstab = {}
samba = {}

for line in os.popen('lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL').read().split('\n'):
    if not line: continue
    if not 'MYBOOK' in line :continue
    try:
        dev,form,s,name = line.split()
        samba[name] = 1
    except:
        dev,form,s,mp,name = line.split()
        samba[name] = 1
        print mp,"already mounted"
        continue
        os.system('umount %s'%mp)
    dev = dev[-4:]
    print name,"on",dev
    fstab[dev] = name

os.system('cp /etc/fstab.base fstab_new')
n = open('fstab_new','a')
for dev,name in fstab.items():
    mnt='/mnt/%s'% name
    os.system('mkdir -p %s'% mnt)
    opt='defaults,noauto'
    add='/dev/%s %s %s %s 0 0 \n'%(dev, mnt, form, opt)
    n.write( add )
n.close()
os.system('mv fstab_new /etc/fstab')

for _,name in fstab.items():
    mnt='/mnt/%s'% name
    os.system('umount %s'%mnt)
    print "mounting",mnt
    os.system('mount %s'%mnt)
    

os.system('cp /etc/samba/smb.conf.base samba_new')
n = open('samba_new','a')
for name in samba:
    print "configuring samba for",name
    n.write("""[%s]
    comment = %s served over pi
    path = /mnt/%s
    browseable = yes
    guest ok = yes
    read only = no
    create mask = 0755

"""%(name, name, name ))
n.close()
os.system('mv samba_new /etc/samba/smb.conf')
os.system('systemctl restart smbd.service nmbd.service')
