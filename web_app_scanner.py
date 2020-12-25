from tld import get_tld
import urllib.request
import argparse
import io
import os
 
ROOT_DIR = 'Websites'

print('''

$$\      $$\           $$\               $$$$$$\                             $$$$$$\                                                             
$$ | $\  $$ |          $$ |             $$  __$$\                           $$  __$$\                                                            
$$ |$$$\ $$ | $$$$$$\  $$$$$$$\         $$ /  $$ | $$$$$$\   $$$$$$\        $$ /  \__| $$$$$$$\ $$$$$$\  $$$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\  
$$ $$ $$\$$ |$$  __$$\ $$  __$$\        $$$$$$$$ |$$  __$$\ $$  __$$\       \$$$$$$\  $$  _____|\____$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ 
$$$$  _$$$$ |$$$$$$$$ |$$ |  $$ |       $$  __$$ |$$ /  $$ |$$ /  $$ |       \____$$\ $$ /      $$$$$$$ |$$ |  $$ |$$ |  $$ |$$$$$$$$ |$$ |  \__|
$$$  / \$$$ |$$   ____|$$ |  $$ |       $$ |  $$ |$$ |  $$ |$$ |  $$ |      $$\   $$ |$$ |     $$  __$$ |$$ |  $$ |$$ |  $$ |$$   ____|$$ |      
$$  /   \$$ |\$$$$$$$\ $$$$$$$  |       $$ |  $$ |$$$$$$$  |$$$$$$$  |      \$$$$$$  |\$$$$$$$\\$$$$$$$ |$$ |  $$ |$$ |  $$ |\$$$$$$$\ $$ |      
\__/     \__| \_______|\_______/$$$$$$\ \__|  \__|$$  ____/ $$  ____/$$$$$$\ \______/  \_______|\_______|\__|  \__|\__|  \__| \_______|\__|      
                                \______|          $$ |      $$ |     \______|                                                                   
                                                  $$ |      $$ |                                                                                
                                                  \__|      \__|                                                                                
$$$$$$$\                                 $$\                                     $$\           $$\                                      
$$  __$$\                                $$ |                                    $$ |          $$ |                                     
$$ |  $$ | $$$$$$\  $$\    $$\  $$$$$$\  $$ | $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$$ |          $$$$$$$\  $$\   $$\ $$\                  
$$ |  $$ |$$  __$$\ \$$\  $$  |$$  __$$\ $$ |$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$ |          $$  __$$\ $$ |  $$ |\__|                 
$$ |  $$ |$$$$$$$$ | \$$\$$  / $$$$$$$$ |$$ |$$ /  $$ |$$ /  $$ |$$$$$$$$ |$$ /  $$ |          $$ |  $$ |$$ |  $$ |                     
$$ |  $$ |$$   ____|  \$$$  /  $$   ____|$$ |$$ |  $$ |$$ |  $$ |$$   ____|$$ |  $$ |          $$ |  $$ |$$ |  $$ |$$\                  
$$$$$$$  |\$$$$$$$\    \$  /   \$$$$$$$\ $$ |\$$$$$$  |$$$$$$$  |\$$$$$$$\ \$$$$$$$ |          $$$$$$$  |\$$$$$$$ |\__|                 
\_______/  \_______|    \_/     \_______|\__| \______/ $$  ____/  \_______| \_______|          \_______/  \____$$ |                     
                                                       $$ |                                              $$\   $$ |                     
                                                       $$ |                                              \$$$$$$  |                     
                                                       \__|                                               \______/                      
$$$$$$$$\   $$\    $$$$$$\      $$$$$$$$\                                                                                                      
$$  _____|$$$$ |  $$  __$$\     \__$$  __|                                                                                                     
$$ |      \_$$ |  \__/  $$ |       $$ | $$$$$$\   $$$$$$\  $$$$$$\$$$$\                                                                        
$$$$$\      $$ |   $$$$$$  |       $$ |$$  __$$\  \____$$\ $$  _$$  _$$\                                                                       
$$  __|     $$ |  $$  ____/        $$ |$$$$$$$$ | $$$$$$$ |$$ / $$ / $$ |                                                                      
$$ |        $$ |  $$ |             $$ |$$   ____|$$  __$$ |$$ | $$ | $$ |                                                                      
$$ |      $$$$$$\ $$$$$$$$\        $$ |\$$$$$$$\ \$$$$$$$ |$$ | $$ | $$ |                                                                      
\__|      \______|\________|$$$$$$\\__| \_______| \_______|\__| \__| \__|                                                                      
                            \______|                                                                                                           
                                                                                                                                                                                                                                                                            
''')
 
def create_dir(directory, quiet=False):
    if not os.path.exists( directory ):
        if not quiet:
            print( "Creating new directory, '{}'.".format( directory ) )
 
        os.makedirs( directory )
 
    else:
        if not quiet:
            print( "Directory allready exists, '{}'.".format( directory ) )
 
def write_file(path, data, quiet=False):
    if not quiet:
        print( "Writing '{}'.".format( path ) )
 
    with open( path, 'w' ) as file:
        file.write( data )
 
def get_domain_name(url, quiet=False):
    if not quiet:
        print( "Getting domain name,'{}'.".format( url ) )
 
    return get_tld( url, as_object=True ).fld
 
def get_ip_address(url, quiet=False):
    if not quiet:
        print( "Getting ip address from '{}'.".format( url ) )
 
    process = os.popen( 'host {}'.format( url ) )
    
    process_data = process.read()
    
    result = process_data.splitlines()

    ip_addresses = []

    for line in result:
        if line.find( 'has address' ) != -1:
            marker = line.find( 'has address' ) + 12
            ip_addresses.append(str(line)[marker:])
 
    return ip_addresses
 
def get_nmap(options, ip, quiet=False):
    if not quiet:
        print( "Performing 'nmap' scan on {}".format( ', '.join(ip) ) )
 
    process = os.popen( "nmap {0} {1}".format( options, ' '.join(ip) ) )
    result = str( process.read() )
 
    return result
 
def get_robots_txt(url, quiet=False):
    if not quiet:
        print( "Downloading 'robot.txt' from '{}'".format( url ) )
 
    if not url.endswith( '/' ):
        url += '/'
 
    request = urllib.request.urlopen( '{}robots.txt'.format( url ), data=None )
    data = io.TextIOWrapper( request, encoding='utf-8' )
 
    return data.read()
 
def get_whois(domain_name, quiet=False):
    if not quiet:
        print( "Getting 'whois' info from '{}'.".format( domain_name ) )
 
    process = os.popen( 'whois {}'.format( domain_name ) )
    result = str( process.read() )
 
    return result

def get_dig(ip, quiet=False):
    if not quiet:
        print( "Performing 'dig' scan on {}".format( ', '.join(ip) ) )
 
    process = os.popen( "dig {}".format( ', '.join(ip) ) )
    result = str( process.read() )
 
    return result

def get_reverse_dns(ip, quiet=False):
    if not quiet:
        print( "Performing 'reverse DNS' scan on {}".format( ', '.join(ip) ) )
 
    process = os.popen( "dig +short -x {}".format( ' '.join(ip) ) )
    result = str( process.read() )
 
    return result

def get_sqlmap(domain_name, quiet=False):
    if not quiet:
        print( "Getting 'sqlmap' info from '{}'.".format( domain_name ) )
 
    process = os.popen( 'sqlmap -u {} --forms --crawl=5 --batch'.format( domain_name ) )
    result = str( process.read() )
 
    return result

def get_commix(domain_name, quiet=False):
    if not quiet:
        print( "Getting 'commix' info from '{}'.".format( domain_name ) )
 
    process = os.popen( 'commix -u https://{} --batch --level=3'.format( domain_name ) )
    result = str( process.read() )
 
    return result

def get_cmsmap(domain_name, quiet=False):
    if not quiet:
        print( "Getting 'cmsmap' info from '{}'.".format( domain_name ) )
    
    process = os.popen( 'cmsmap -F https://{}'.format( domain_name ) )
    result = str( process.read() )
 
    return result


def gather_info(url, quiet=False):
 
    print( "Gathering info from '{}'.".format( url ) )
 
    try:
        domain_name = get_domain_name( url, quiet )
    except:
        print('Whoops')
        domain_name = 'Whoops'
    try:
        ip_address = get_ip_address( domain_name, quiet )
    except:
        print('Whoops')
        ip_address = 'Whoops'
    try:
        nmap = get_nmap( '-F', ip_address, quiet )
    except:
        print('Whoops')
        nmap = 'Whoops'
    try:
        dig = get_dig( ip_address, quiet )
    except:
        print('Whoops')
        dig = 'Whoops'
    try:
        reverse_dns = get_reverse_dns( ip_address, quiet )
    except:
        print('Whoops')
        reverse_dns = 'Whoops'
    try:
        ip_address = str('\n'.join(ip_address))
    except:
        print('Whoops')
        ip_address = 'Whoops'
    try:
        robots_txt = get_robots_txt( url, quiet )
    except:
        print('Whoops')
        robots_txt = 'Whoops'
    try:
        whois = get_whois( domain_name, quiet )
    except:
        print('Whoops')
        whois = 'Whoops'
    try:
        sqlmap = get_sqlmap( domain_name, quiet )
    except:
        print('Whoops')
        sqlmap = 'Whoops'
    try:
        commix = get_commix( domain_name, quiet )
    except:
        print('Whoops')
        commix = 'Whoops'
    try:
        cmsmap = get_cmsmap( domain_name, quiet )
    except:
        print('Whoops')
        cmsmap = 'Whoops'
    
 
    data = {
        'domain_name':domain_name, 'ip_address':ip_address, 'nmap':nmap, 'dig':dig, 'reverse_dns':reverse_dns,
        'robots_txt':robots_txt, 'whois':whois, 'sqlmap':sqlmap, 'commix':commix, 'cmsmap':cmsmap,
    }
 
    create_report( data, quiet )
 
def create_report( data, quiet ):
    project_dir = '{0}/{1}'.format( ROOT_DIR, data['domain_name'] )
    create_dir( project_dir, quiet )
 
    print( "Savign report in '{}'.".format( project_dir ) )
 
    for key, value in data.items():
        file = '{0}/{1}.txt'.format( project_dir, key )
 
        if not quiet:
            print( 'Savign {}'.format( file ) )
 
        write_file( file, value, quiet )
 
 
    print( "Done with '{}'.\n".format( data['domain_name'] ) )
 
def Main():
    create_dir( ROOT_DIR )
 
    parser = argparse.ArgumentParser()
 
    parser.add_argument('url_list', help='website to gather info.', type=str )
    parser.add_argument('-l', '--list', help='<url> is website list.', action='store_true' )
    parser.add_argument('-q', '--quiet', help='silent mode.', action='store_true' )
 
    args = parser.parse_args()
 
    if args.url_list and not args.list:
        gather_info( args.url, args.quiet )
 
    elif args.url_list and args.list:
        print( "Loading website list '{}'".format( args.url_list ) )
 
        with open( args.url_list, 'r' ) as file:
            data = file.read().split('\n')[:-1]
 
            for line in data:
                gather_info( line, args.quiet )
 
        print( "Done with website list '{}'.\n".format( args.url_list ) )
 
if __name__ == '__main__':
    Main()