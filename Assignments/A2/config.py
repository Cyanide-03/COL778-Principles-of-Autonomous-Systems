
'''
This file contains the configs used for Model creation and training. You need to give your best hyperparameters and the configs you used to get the best results for 
every environment and experiment.  These configs will be automatically loaded and used to create and train your model in our servers.
'''
#You can add extra keys or modify to the values of the existing keys in bottom level of the dictionary.
#DO NOT CHANGE THE STRUCTURE OF THE DICTIONARY. 

configs = {
    
    'Hopper-v4': {
            #You can add or change the keys here
              "hyperparameters": {
                'batch_size': 512,
                "num_iteration":250,
                "max_length":1000, # max episode length (episode is one rollout)
                "num_trajs":10, # (number of episodes for each iteration)
                "n_layers":2,
                "size":64,
                "lr":1e-3
            },
            "num_iteration": 250,
            "episode_len": 1000
    },
    
    
    'Ant-v4': {

              "hyperparameters": {
                'batch_size': 512,
                "num_iteration":500,
                "max_length":1000,
                "num_trajs":10,
                "n_layers":2,
                "size":64,
                "lr":1e-3
            },
            "num_iteration": 500,
            "episode_len": 1000

    }

}