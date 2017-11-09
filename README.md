# Grafana Operator
A script that you can do some actions to grafana server.


### required options:

##### --url http://url:port
 - grafana url and port

##### --action enable|export|import
 - enable: enable "monitor" app and delete dashboards in default organization for now.
 - export: export default organization dashboards to current directory.
 - import: import dashboards form current directory to default organization.

##### --app id (when action is enable)
 - id: app id in plugin.json

### usage:
```
chmod +x grafana_operator.py
./grafana_operator.py --url http://192.168.33.101:3000 --action export
./grafana_operator.py --url http://192.168.33.101:3000 --action import
./grafana_operator.py --url http://192.168.33.101:3000 --action enable
./grafana_operator.py --url http://192.168.33.101:3000 --action enable --app alexanderzobnin-zabbix-app
```
