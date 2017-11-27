import Player
import GameEngine
from BuildInfo import BuildInfo
import HostControl
# import pdb; pdb.set_trace()

# functions to broadcast gamestate changes
def broadcast_message(message):
    for player in game_engine.game_state.player_array:
        host.send_data(player.netid[0], message)

def broadcast_resources():
    for player in game_engine.game_state.player_array:
        host.send_data(player.netid[0], ' '.join(['rsrc'+str(player.inventory.brick),
                                                  str(player.inventory.grain),
                                                  str(player.inventory.lumber),
                                                  str(player.inventory.ore),
                                                  str(player.inventory.wool)]))

def make_build_info(request):
    if request[:4] == 'road':
        return BuildInfo(int(request[4]), int(request[5]), int(request[6]), True, False, False)
    elif request[:4] == 'sett':
        return BuildInfo(int(request[4]), int(request[5]), int(request[6]), False, True, False)
    elif request[:4] == 'devc':
        return BuildInfo(0, 0, 0, False, False, True)
    elif request[:4] == 'pass':
        return None
    else:
        # TODO: raise a damn error
        return None

# get player connections
host = HostControl.HostControl(('localhost', 8000))
player_addrs = host.get_conns()

# initialize players
player_array = []
netid = player_addrs[0]
player1 = Player.Player(netid, 'blue', 'blue')
netid = player_addrs[1]
player2 = Player.Player(netid, 'red', 'red')
player_array.append(player1)
player_array.append(player2)
for player in player_array:
    player.inventory.lumber += 400
    player.inventory.brick += 400
    player.inventory.wool += 200
    player.inventory.grain += 200

# initialize game
game_engine = GameEngine.GameEngine(player_array)

# build initial 'beginner' setup
game_engine.build(BuildInfo(0, 0, 3, False, True, False))
broadcast_message('sett003')
game_engine.build(BuildInfo(3, 2, 2, False, True, False))
broadcast_message('sett322')
game_engine.build(BuildInfo(0, 0, 2, True, False, False))
broadcast_message('road002')
game_engine.build(BuildInfo(3, 2, 2, True, False, False))
broadcast_message('road322')
game_engine.next_player()
game_engine.build(BuildInfo(1, 1, 2, False, True, False))
broadcast_message('sett112')
game_engine.build(BuildInfo(2, 2, 2, False, True, False))
broadcast_message('sett222')
game_engine.build(BuildInfo(1, 1, 1, True, False, False))
broadcast_message('road111')
game_engine.build(BuildInfo(2, 2, 2, True, False, False))
broadcast_message('road222')
game_engine.next_player()

# start first player's turn and roll first dice
host.send_data(game_engine.game_state.current_player.netid[0], 'strt')
roll = game_engine.dice_roll()
broadcast_message('roll{}'.format(roll))
broadcast_resources()

# game loop
while True:
    if not host.requests.empty():
        print('<<< reading request')
        current_request = host.requests.get()
        requester_netid = current_request[0]
        if requester_netid == game_engine.game_state.current_player.netid:
            build_info = make_build_info(current_request[1])
            if build_info is not None:
                print(current_request)
                if game_engine.build(build_info):
                    print('>>> broadcasting success')
                    for vertex in game_engine.game_state.invalid_vertices_to_build_array:
                        print(vertex)
                    broadcast_resources()
                    broadcast_message(current_request[1])
                else:
                    print('>>> sending error')
                    for vertex in game_engine.game_state.invalid_vertices_to_build_array:
                        print(vertex)
                    host.send_data(current_request[0][0], 'errr')
            else:
                print('>>> ending {}\'s turn'.format(game_engine.game_state.current_player.name))
                host.send_data(current_request[0][0], 'endt')
                game_engine.next_player()
                print('>>> updating resources and alerting players')
                roll = game_engine.dice_roll()
                print('>>> sending roll: {}'.format(roll))
                broadcast_resources()
                broadcast_message('roll{}'.format(roll))
                print('>>> starting {}\'s turn'.format(game_engine.game_state.current_player.name))
                host.send_data(game_engine.game_state.current_player.netid[0], 'strt')
