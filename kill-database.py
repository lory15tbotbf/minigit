#!/usr/bin/env python2

from minigit import db
from minigit.models import *
from minigit.util import generate_authorized_keys

db.drop_all()
db.create_all()

### USERS
admin = User("admin", "test01")
admin.is_admin = True
admin.addEmail("test@example.com", True, True)
# admin.addPublicKey("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDRUFLcksSX57IC7Z1yGWWYignX7tnn0c2EffImrZbUoZTtxpQPvsnkw191/NAb9ol8K0ndjLYtaaRIxYsXwAcLaT+/Cu0K+Jd7E+CKa1KzJJNhYsnEJIYH+JMFbBcq3IP+r5XI5E35SA0mjWlPHmqFDssotSPd9f0Q66OIy7MNscrJaNNUSauVkNVr/SlMpEHB0mpY0fZJZz0Qlqb2PV7OWvh332bMdM70+dl9CyxNRNruApq95gI+IUYac7gMqgtoFIsxojBvaETuMqqhcfwuc9wx++ezxqq2UgMV9KDGlv9rfrjPr+P3/ZhUD0afo75BalCLyEAVeYugCv8hRg+lD1IgT7oJy1WVPIKAHgM8KjqDKWUDBJRdnBokMQ/y8PEaGRBzpWk5YIWefDf901xosgi4L+DMr2fxb7wRJOLb88Y+MmBuaN5ODa6FGMo7Ql7xRwgbVleS+J46mr2HG7ITTSLvn5on7K3cAfvUQsFfcesYLoHGbL6Lf7VY7HxAEMxrj9QJyp3LWrHw7kTdxGsT34ZQCcbI4NM0h++LVer5yjlMgOM8yf5ehc6hMIj2s417HNBKWMeojyZG3ThvtmQmhvxVyrWdFhntNB0tB0RxMiINQEBHLV6S/OHg9TKEhcPn1csG8H2QjXf1k88cGjuFu6xzCam+0Hfk/2DDZmkRVQ== paul@newton")
db.session.add(admin)

opatut = User("opatut", "test01")
opatut.addEmail("opatutlol@aol.com", True, True)
opatut.addEmail("paulbienkowski@aol.com")
opatut.addPublicKey("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDRUFLcksSX57IC7Z1yGWWYignX7tnn0c2EffImrZbUoZTtxpQPvsnkw191/NAb9ol8K0ndjLYtaaRIxYsXwAcLaT+/Cu0K+Jd7E+CKa1KzJJNhYsnEJIYH+JMFbBcq3IP+r5XI5E35SA0mjWlPHmqFDssotSPd9f0Q66OIy7MNscrJaNNUSauVkNVr/SlMpEHB0mpY0fZJZz0Qlqb2PV7OWvh332bMdM70+dl9CyxNRNruApq95gI+IUYac7gMqgtoFIsxojBvaETuMqqhcfwuc9wx++ezxqq2UgMV9KDGlv9rfrjPr+P3/ZhUD0afo75BalCLyEAVeYugCv8hRg+lD1IgT7oJy1WVPIKAHgM8KjqDKWUDBJRdnBokMQ/y8PEaGRBzpWk5YIWefDf901xosgi4L+DMr2fxb7wRJOLb88Y+MmBuaN5ODa6FGMo7Ql7xRwgbVleS+J46mr2HG7ITTSLvn5on7K3cAfvUQsFfcesYLoHGbL6Lf7VY7HxAEMxrj9QJyp3LWrHw7kTdxGsT34ZQCcbI4NM0h++LVer5yjlMgOM8yf5ehc6hMIj2s417HNBKWMeojyZG3ThvtmQmhvxVyrWdFhntNB0tB0RxMiINQEBHLV6S/OHg9TKEhcPn1csG8H2QjXf1k88cGjuFu6xzCam+0Hfk/2DDZmkRVQ== paul@newton")
db.session.add(opatut)

zetaron = User("zetaron", "test01")
zetaron.addEmail("fabian.stegemann@gmx.net", True, True)
zetaron.addPublicKey("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC2YAj5i7PiANi0OuNEoi2DlPYVFhAN6pAOwm06bI1htIy2/Em0QLAHFuf5+v4Ty5AFTGdSAWK2zB3KDJOfEJ5GWgPkeIKo/MNzFD8BBYgbFC8y+jW6e0JrhaTiB6PJ0xbxepUZzqIp5NpL4i/BN3+8cCQf+Ny8J5P2tMPour03iSvsyFQAILnpThD0lljyW6a7Xc1+5ZSITLTHMfdxruyBhnUOuz8IcxHknKTwJSK1q7Yg5x3cpBz3K7IOLsnwMHSPhtPD1SuFxMUevbGYGr9A99R+zarghNZNXKCe0R7ui3l9frVLwSnMHW4/mKuQDKUMwNmpyHYpfwljTq0qnPlXNIxG46VIvfhmt9FiFNQWQQYIOCSMDIZAfLu9PJcjvHzVD5bZIMsQYfCeYAQz9IwGqhNIJKG8Cj7gFm5F7iAKHOo50wwAfZEChTGv6VWOQJmOTaBkRW6gnB/x39+WXhkYOISW/5BZYRQsUWUf9tnIBjml+cJX/7+hIUC/MG0AK+mknziISZW09gnrlD4BGZ1Fxarcv0owiK5fJy9c4KuBzBOwgvtC35XPDTlpxuqh/89b9fAoWEYjp6bW/AsWKtw6s8IpRWZzPDUBguXunjUAV16m+mgwFH2XJKM5zK1f/vJY+TXN2dpi0nL1ELztwe1SobsFQA9cq4VG1dIq0S8MlQ== fabian@zetarania")
db.session.add(zetaron)

nobody = User("nobody", "test01")
nobody.addEmail("nobody@example.com", True, True)
# nobody.addPublicKey("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDRUFLcksSX57IC7Z1yGWWYignX7tnn0c2EffImrZbUoZTtxpQPvsnkw191/NAb9ol8K0ndjLYtaaRIxYsXwAcLaT+/Cu0K+Jd7E+CKa1KzJJNhYsnEJIYH+JMFbBcq3IP+r5XI5E35SA0mjWlPHmqFDssotSPd9f0Q66OIy7MNscrJaNNUSauVkNVr/SlMpEHB0mpY0fZJZz0Qlqb2PV7OWvh332bMdM70+dl9CyxNRNruApq95gI+IUYac7gMqgtoFIsxojBvaETuMqqhcfwuc9wx++ezxqq2UgMV9KDGlv9rfrjPr+P3/ZhUD0afo75BalCLyEAVeYugCv8hRg+lD1IgT7oJy1WVPIKAHgM8KjqDKWUDBJRdnBokMQ/y8PEaGRBzpWk5YIWefDf901xosgi4L+DMr2fxb7wRJOLb88Y+MmBuaN5ODa6FGMo7Ql7xRwgbVleS+J46mr2HG7ITTSLvn5on7K3cAfvUQsFfcesYLoHGbL6Lf7VY7HxAEMxrj9QJyp3LWrHw7kTdxGsT34ZQCcbI4NM0h++LVer5yjlMgOM8yf5ehc6hMIj2s417HNBKWMeojyZG3ThvtmQmhvxVyrWdFhntNB0tB0RxMiINQEBHLV6S/OHg9TKEhcPn1csG8H2QjXf1k88cGjuFu6xzCam+0Hfk/2DDZmkRVQ== paul@newton")
db.session.add(nobody)

### REPOSITORIES
test = Repository("Test Repository", "test")
db.session.add(test)
test.init()

minigit = Repository("Minigit", "minigit")
db.session.add(minigit)
minigit.init()
db.session.commit()

### PERMISSIONS
test.setUserPermission(opatut, "admin")
test.setUserPermission(zetaron, "read")
minigit.setUserPermission(opatut, "admin")
db.session.commit()

### ISSUES
i1 = Issue(test, "Something is wrong here")
db.session.add(i1)
i2 = Issue(test, "Dude you broke it")
db.session.add(i2)
db.session.commit()

i1.reply("Something is really, really, horribly broken, as it seems. Maybe. *Fun fun fun*!", opatut)
i2.reply("Somebody is retard.", zetaron)
i2.reply("That must be you.", opatut)
i2.close(opatut)

## Issue Tags

tagBug = IssueTag("Bug", "#F00", test)
tagFeature = IssueTag("Feature", "#2C3", test)
tagDocumentation = IssueTag("Docs", "#AAA", test)
tagCleanup = IssueTag("Cleanup", "#A0A", test)
db.session.add(tagBug)
db.session.add(tagFeature)
db.session.add(tagDocumentation)
db.session.add(tagCleanup)
db.session.commit()
i1.tags.append(tagBug)
i1.tags.append(tagCleanup)
db.session.commit()



### FINISH
generate_authorized_keys()
