# requirements

-> python>=3.10

-> aiogram>=3.0
    - framework for developing telegram bot

-> schedule
    - for crating scheduled scripts that run at specific time 

-> pyee
    - event emitter package that used with schedule library

-> aiogram-datepicker(optional)
    - datepicker widgets for aiogram framework

-> aiogram-timepicker(optional)
    - timepicker widgets for aiogram framework

-> aiogram_widgets(optional)
    - pagination widgets for aiogram framework


# folder structure

<pre>
├── documentation
│   ├── user_doc
│   ├── system_doc
│   └── code_doc
├── helpers
│   ├── bot_runner.py
│   ├── event_storage.py
│   └── executor.py
├── routers
│   ├── {rout_name}.py
│   └── routes.py
├── controllers
│   └── {controller_name}.py
├── models
│   └── {model_name}.py   
├── scheduler_events
│   ├── {schedule_script_name}.py
│   └── schedules.py
└── web_app
│   └── web_app_routes.py
├── {project_other_folder/package/module}
│   ├── {its file.py}
├── readme.md
├── requirements.txt
├── .config
├── main.py
</pre>


# main.py
- is file that used as to run your bot or project
# modal
# scheduler_events....
