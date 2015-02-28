from m_engine import *
import utils, states, scenes

"""
Basic example of implementation of the engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Controls:
arrows and wsad
tab to toggle camera focus
~~~~~~~~~~~~~~~~
"""

isShiyang = utils.getCurrentUsername().lower() in  ("shiyang", "sean")

#initialize the engine and AssetManager
Engine.init(displayFlags = [] if isShiyang else [])
Engine.setTitle("Mustang Cannon!")
AssetManager.init("Assets/assetConfig.ini")

Engine.state = "Game" if isShiyang else "Menu"

#Add the menu state into the engine
Engine.addState(states.Menu(),"Menu")

#Add the game state into the engine
Engine.game = states.Playing()

#load in the front rotunda; note that the loading in should be done
#by the menuhandler when they click front rotunda
Engine.game.space.loadScene(scenes.FrontRotunda())
Engine.addState(Engine.game,"Game") 

Engine.run()
