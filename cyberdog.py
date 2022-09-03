# CyberDog 
# Kevin McAleer
# September 2022

from phew import server, template, logging, access_point, dns
from phew.template import render_template
from phew.server import redirect
import gc
gc.threshold(50000)

DOMAIN = "pico.wireless"

@server.route("/", methods=['GET','POST'])
def index(request):
    if request.method == 'GET':
        logging.debug("Get request")
        return render_template("index.html")
    if request.method == 'POST':
        text = request.form.get("text", None)
        logging.debug(f'posted message: {text}')
        return render_template("index.html", text=text)

@server.route("/wrong-host-redirect", methods=["GET"])
def wrong_host_redirect(request):
  # if the client requested a resource at the wrong host then present 
  # a meta redirect so that the captive portal browser can be sent to the correct location
  body = "<!DOCTYPE html><head><meta http-equiv=\"refresh\" content=\"0;URL='http://" + DOMAIN + "'/ /></head>"
  logging.debug("body:",body)
  return body

@server.route("/hotspot-detect.html", methods=["GET"])
def hotspot(request):
    return render_template("index.html")

@server.catchall()
def catch_all(request):
    if request.headers.get("host") != DOMAIN:
        return redirect("http://" + DOMAIN + "/wrong-host-redirect")

# Set to Accesspoint mode
ap = access_point("Wifi In The Woods")
ip = ap.ifconfig()[0]
logging.info(f"starting DNS server on {ip}")
dns.run_catchall(ip)
server.run()
logging.info("Webserver Started")
