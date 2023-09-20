# webApp
from aiohttp.web_app import Application
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web import run_app

class BotRunner:
    def __init__(self,Dispatcher,Bot,Host,Port,webhookPath) -> None:
        self.Dispatcher = Dispatcher
        self.Bot = Bot
        self.App = Application()
        self.webhookPath = webhookPath
        self.Host = Host
        self.Port = Port
    
    def webApp(self):
        self.App['bot'] = self.Bot
        return self.App
    
    def run(self):
        SimpleRequestHandler(
        dispatcher=self.Dispatcher,
        bot=self.Bot
        ).register(self.App,path=self.webhookPath)
        
        setup_application(self.App,self.Dispatcher,bot=self.Bot)
        
        run_app(app=self.App,host=self.Host,port=self.Port)