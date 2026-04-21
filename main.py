import sys
from agent import Agent
from board import Board
from tourParTour import play_visual, play_multiple_visual

ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def parse_args(argv):
	args = {
		"sessions": 0,
		"save": None,
		"load": None,
	    "visual": True,      # -visual on/off
		"dontlearn": False,  # -dontlearn
		"step_by_step": False, # -step-by-step
		"visual_play": False,  # -visual-play pour lancer la visualisation graphique
		"visual_games": 1    # -visual-games n pour jouer n parties avec visualisation
	}
	index = 1
	while index < len(argv):
		argument = argv[index]
		if argument == "-sessions" and index + 1 < len(argv):
			args["sessions"] = int(argv[index + 1])
			index += 2
		elif argument == "-save" and index + 1 < len(argv):
			args["save"] = argv[index + 1]
			index += 2
		elif argument == "-load" and index + 1 < len(argv):
			args["load"] = argv[index + 1]
			index += 2
		elif argument == "-visual" and index + 1 < len(argv):
			args["visual"] = argv[index + 1] == "on"
			index += 2
		elif argument == "-dontlearn":
			args["dontlearn"] = True
			index += 1
		elif argument == "-step-by-step":
			args["step_by_step"] = True
			index += 1
		elif argument == "-visual-play":
			args["visual_play"] = True
			index += 1
		elif argument == "-visual-games" and index + 1 < len(argv):
			args["visual_games"] = int(argv[index + 1])
			index += 2
		else:
			index += 1
	print(args)
	return args

def train(episodes, agent=None):
	if agent is None:
		agent = Agent()

	for i in range(episodes):
		board = Board()
		done = False
		state = board.get_state()
		visited = {}
		steps = 0
		while not done:
			if state in visited:
				visited[state] += 1
				if visited[state] > 3:
					reward_extra = -1
				else:
					reward_extra = 0
			else:
				visited[state] = 1
				reward_extra = 0
			action_index = agent.choose_action(state)
			direction = ACTIONS[action_index]
			done, reward = board.move(direction)
			reward += reward_extra
			next_state = board.get_state()
			agent.update(state, action_index, reward, next_state, done)
			state = next_state
			steps +=1
		agent.epsilon = max(agent.epsilon_min, agent.epsilon * agent.epsilon_decay)

		if (i % 1000 == 0):
			print(f"Episode {i} | epsilon: {agent.epsilon:.3f} | Q-table size: {len(agent.Q_table)}")			
	return agent

def evaluate(agent, episodes=10):
    win = 0
    agent.epsilon = 0
    for i in range(episodes):
        board = Board()
        done = False
        state = board.get_state()
        steps = 0
        while not done and steps < 500:
            action_idx = agent.choose_action(state)
            direction = ACTIONS[action_idx]
            done, reward = board.move(direction)
            next_state = board.get_state()
            state = next_state
            steps += 1
        length = len(board.snake)
        print(f"Session {i+1}: longueur={length}, steps={steps}")
        if length >= 10:
            win += 1
    print(f"\n{win}/10 sessions avec longueur >= 10")

def main():
	args = parse_args(sys.argv)
	agent = Agent()
	if args["load"]:
		agent.load(args["load"])
	if args["sessions"] > 0:
		agent = train(args["sessions"], agent)
	if args["save"]:
		agent.save(args["save"])
	
	# Mode visualisation graphique
	if args["visual_play"]:
		if args["visual_games"] > 1:
			play_multiple_visual(agent, num_games=args["visual_games"])
		else:
			board = Board()
			play_visual(agent, board, step_by_step=args["step_by_step"])
	else:
		# Évaluation standard
		evaluate(agent)
	
	return 0

if __name__ == "__main__":
	main()