How to use:

```
pip install -r requirements.txt
cp agent_voe.py <path/to/mcs_eval3>
cp agent_util.py <path/to/mcs_eval3>
python agent_voe.py
```

The functionality for the evaluation only requires those 2 files. The others are  included in case someone finds them useful...

It has also been built and tested inside mcs_eval3, not in this git repo. 

You will also need to correct the location of the json scene files in agent_voe.py:

```
env = McsEnv(
    task="eval3_dataset", scene_type="agent_obj_preference", seed=50,
    start_scene_number=0, frame_collector=collector, set_trophy=False
)
```
