get up vector working correctly

~~implement a pipeline of actions~~

~~get player working correctly~~

~~callbacks, fireball, mage~~

~~set hitpoints for fireball and attack and units~~

~~setup magic so that it is number of spells based rather than mana based(flexible based on passed object)~~

reorganize file structure so that it uses individual directories for the map/playerlist/etc -- add a place for campaigns

~~add a few more units and build the computer's ability to attack so that you can have a demo of two cpus going at it - for this the cpu should assign a value to attack and then look through all the traits and either decide to attack or use traits based on a getStrength() function in the trait object that can be later refactored to be automatic.~~

add refreshing abilities in traits

~~modify dotscene to import terrain meshes
(might not require modification actually)~~

> grab all objects in an area to have a mass effect - (a box of raycasts that return alist or a gigantic created body with the collisions returning a list,( or just iterate through and find anything within a certain box, do the third))

~~refactor out the interface in player to a seperate object~~

~~define the attributes of a trait so that a cpu can determine the strongest (eg area effect, range, damage, other effects and make it so that you can easily make a lot of traits and have a cpu that works.(started)~~

~~build a scene in blender based on dr disaster of gunn court based on the two previous models I have - setup scene, setup ogre scene exporter~~

check out rosegarden for music

~~attach light to fireball(hard to see with lights)~~

add a camera property that makes it start out focusing on a particular unit or just have it move to focus on the next unit on the next turn

fix the scene scale as the meshes default to 3x as large as the bodies

~~finish the scene, make sure cpus attack back and forth and that you have a working scene~~

figure out scene materials

~~design a simple event system~~with just a turn 0,1,2,3 show dialogue option

~~set overall value for traits~~

~~make only one trait usable per turn aside from traits with action=False(only done for cpu~~

~~Put move and attack into generic traits modules, this was having problems with old pyc files or something maybe(I think it was actually wierd naming issues.  Didn't really fix~~

todo - learn how to calculate trajectory
jump attack
~~min max range distance function already built, simply apply it.~~
long range short range attack, one lobbed
~~realtime movement - every unit has its own action queue~~

~~move physics utilities into own class~~

on start turn event
on attack event

~~check damage based on unit~~

~~make the cpu move to find the correct distance (close or far) and attack~~

~~add health counter(maybe not done)~~

http://www.cs.ucr.edu/~macchiea/cs134/lab1/ogrehelp/ogremeshesexporter.html texture meshes

~~initial velocity = square root(range **gravity/sin(2** degrees)
Quaternion quat = Quaternion(Degree(45),Vector3::UNIT\_Y)
velocity = sqrt(distance(vec1,vec2) **9.8 / sin(2** 45))
set rotation, set velocity and the resulting trajectory should hit the enemy unit(figured out over level ground only because thats the formula I used~~

~~add expiring body (range attack is now expiring)~~

~~set debug text for logger~~

~~make each callback unit use its own object(having issues with jump attack)~~

~~consider abstracting out the physics so you could somewhat possbily use a different one.(considered)~~

~~Try up vector with round object to see(no diff)~~





~~setup fog of war~~

~~refactor fog of war(its a unit setting)~~

~~add sounds~~

~~ad animations on attacks(need an obj with animation)~~

have one global callback and find the action to occur based on the type of the hitting unit

setup music through pygame to have a real sound system

add a 5 second timer on actions

~~add events~~ and conversation to scene 1

ogre viewport rendertexture - build a camera that displays on a entity for portals

~~figure out why python random module isn't working(cant have random.py in there)~~

complete basic units for 4 countries
(Zal - steampunk completed basic units) add technologies for spark

(A - Magic has one unit,

redmage, fireball) add rain of fire/firewall/fire salamander(speedy/hot(adds some fire damage)).

add blue mage : flood, confuse,  sleep,turtle

add air mage : tornado, wind blast, zephyr, haste,

add all around fighter.  Boosted with random magic weapons and items

(B - cultural none) - add one unit Its abilities don't cost an action and they boost speed/strength/dexterity.  Its weapons are fists (main) so far.  It should borrow upon the technologies of the other nations like magic/magic items/steampunk items/guns but not too much.  It can boost its respective attributes to make itself good with anything.)

(C - Electronics none )
These units should have slightly different weapons like machine gun/sniper rifle/pistol/rocket launcher.  They should make heavy use of cover to do surprise attacks, but still be ok on open ground at a distance due to range.

make guns fire and do damage even if they miss
add missing for guns and melee weapons

add movabletext or cegui for broadcast(item,unit) in mind http://www.ogre3d.org/wiki/index.php/MovableText

~~create and add event system for move~~

~~add leader~~

~~refactor out background running stuff to turn stuff~~

~~make followers follow on leader~~

~~make sure runqueue is fixed (bug where it added units to the uniqueee always~~

~~see if created units are getting ai properly (test more)~~

add more complex event system with ai taking a large role

add movable text to make stuff look better - movable text at http://www.ogre3d.org/wiki/index.php/MovableText need to recompile python ogre to add in that

~~setup statboosts as afffects~~
~~add races and scales by race~~

~~setup a couple of unit types like wizard, timemage, knight, ninja, priest~~

~~balance those types, give them materials, and use zombie mesh for placeholder~~

~~double attack based on a two second timer for ninja~~
~~added a show attributes for the current player~~

~~setup new random style fft scene~~

~~fix ai (need to fix~~

~~finish potion for chemist~~
make throw not so hacky
~~make throw correctly get damage and such from the affect list and apply it~~
~~figure out why ai is never doing basic attack (basic attack would pick the healing option, set attack to return false on healing)~~

~~made it so that hitpoints cannot be set above max hit points, keep in mind that this means if you set hitpoints before max you get 5 hp~~

finish up damage and get chance to hit
> setup new move so that units only move in cardinal directions
> add a get direction function somehow maybe involving quaternions

a function that gets all valid grid spots and can optionally mark them by creating a box above that spot

a function that says whether or not something is within the range given

a function that gets the shortest distance between two points

a function that does a ray cast the appropriate jump height cast in all directions and returns a list of valid blocks

removed
~~add to the scene parser a data level init function
add a build grid function
take existing move functions and have them work off of a grid
make an get off center(x,y) grid function
make a get up down left right map info function
make createrandom work off of that
setup move so it moves along that~~
a grid was too big a change and a problem.  It requires too much duplication of functionality and adds little benefit.  Plus it is just too difficult with ogre.

make show like the range limiter where it just works off of a range property

edit various catch statements to specifically catch only the exceptions wanted to catch

individual AI for human player

On the AI for fft I think the successful way to duplicate it is to store all the effects of actions in a grid and to build a list of turns (with units and spells) in to the game.

The cpu can then effectively not move into items within the grid, only cast spells that will hit, and also add up damage onto a unit at a specific spot until they are dead.

~~updated to 1.6, need to figure out why red torch isn't working(it was a key word before the particle)~~

path finding - jumping I believe should work, but moving around obstacles is not done yet

itemhandling - need to have a traits that limits based on the items for the chemist

~~cpu squires not moving or attacking  - need to fix that~~

~~make sure that timed objects clean up after they are gone~~

fix event death

~~shift the map for traits over to the human interface~~

~~make the cpu use up abilities when using them~~(test)

make the human player use up an action when using an action

fix markvalid and within range

~~create a basic traits that refactors out most of the duplicate code (like listclasses and makes an iterator that just takes a predicate for the returning of abilities)~~(test)

properties for setting above max hp isn't working.  add later and figure out why

BPC need to figure out the FrameListener issue with runthis.py, see [r189](https://code.google.com/p/tesliz/source/detail?r=189) checkin notes