# RockPaperScissorsWithHandTracking

It is the classical game of Rock, Paper, Scissors but with a twist it's played with Computer using hand tracking. It is made using **Mediapipe**.

# Description

Inspired by a video of **Computer Vison** made by a channel channel called Murtaza's workshop's, his video talks briefly about how to use a module called \***\*Mediapipe\*\*** made by Google.
Using the module you can know the positions of the fingers so tracking those positions you can caluculate Rock, Paper, Scissors.

If you doesn't open a finger i.e position of your tip of index finger is less than position middle part of index finger so it's Rock similarly for Paper and Scissors.

## Demo

![Image](https://github.com/Sarath191181208/RockPaperScissorsWithHandTracking/blob/master/images/Screenshot.png?raw=True)

## Run Locally

Clone the project

```bash
  git clone https://github.com/Sarath191181208/RockPaperScissorsWithHandTracking.git
```

Go to the project directory

```bash
  cd ./RockPaperScissorsWithHandTracking
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Run the project Locally

```bash
  python main.py
```

## References

Murtaza's workshop's Video:
https://www.youtube.com/watch?v=NZde8Xt78Iw

Images are picked from Internet.

## Usage

- Hold your hand in rock position and go above the blue line to start.
- Once the timer starts you get 3 seconds to choose your hand.
- After three seconds the computer detects your hand and your choice and displays your's and it's choice on right.

## Requirements

- python `Make sure to add to path`
- mediapipe `pip install mediapipe`
- opencv ` pip install opencv-python`
- pygame ` pip install pygame`
