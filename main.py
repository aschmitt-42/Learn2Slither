from agent import Agent
from board import Board

ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def train(episodes):
	
	agent = Agent()
	
	for i in range(episodes):
		board = Board()
		done = False
		state = board.get_state()
		steps = 0
		while not done:
			action_index = agent.choose_action(state)
			direction = ACTIONS[action_index]
			done, reward = board.move(direction)
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
	agent = train(10000)
	print("train finish")
	evaluate(agent)
	return 0

main()