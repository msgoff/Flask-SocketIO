import re
f = open('Dockerfile')
data = f.read()
f.close()

resp = re.sub('RUN','sudo',data)
resp = re.sub('WORKDIR','cd',resp)
resp = re.sub('FROM.*','',resp)
cmd = re.findall('ENTRYPOINT\s+\[(.*?)].*?CMD\s+\[(.*?)\]',resp,re.DOTALL)
if cmd:
    cmd = cmd[0]
    cmd = cmd[0].strip() + ' ' + cmd[1].strip()
    cmd = cmd.replace('"','')

resp = re.findall('(.*?)# An ENTRYPOINT',resp,re.DOTALL)
f = open('debian.sh','w')
f.write(resp[0]+cmd)
f.close()
