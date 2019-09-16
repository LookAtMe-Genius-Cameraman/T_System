# Usage

T_System has 4 different ways to control. Strong to weak, respectively:

- Command-line tools
- Remote UI
- Augmented
- Official Stand

First of all excluding command-line tools, all control ways are the user interfaces at the same time and they can be activate with using each other.

### Command-line Tools

Selecting the all user interfaces can make with positional `interface` argument. With `-h` or `--help` flag, all abilities of T_System can be shown. 
But there is few important feature those need the  detailed explanation:

#### Sub-commands

- `remote-ui-authentication`
    - There is a secret administration entry in T_System Remote UI.
    When the user write the correct pattern inside to Wi-Fi ssid and
    password fields, administration authenticate will activated. Initial 
    setting of T_System there is a creator authentication keys. So if 
    you want to be admin for Remote UI, you have to change this secret
    ssid and passwords patterns. With this command:
    
      `t_system remote-ui-authentication --ssid <SSID> --password <PASSWORD>`
    
      You can be create your own secret administration entry.
      
    - `face-encoding`
    
    - `self-update`


### Remote UI
### Augmented
### Official Stand

