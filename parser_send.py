import sh

my_password = "password\n"

my_sudo = sh.sudo.bake("ls", _in=my_password)
my_sudo.ls("root")