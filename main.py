from FarmModel import FarmModel

if __name__ == "__main__":
    model = FarmModel(N=2, W=1)
    for i in range(3):
        model.step()
