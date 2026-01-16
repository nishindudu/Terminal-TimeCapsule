# Terminal Timecapsule
A simple terminal-based application to create and manage time capsules.

## Features
- Create time capsules with messages for the future.
- Fun

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/nishindudu/Terminal-TimeCapsule.git
   ```

2. Navigate to the project directory:
    ```bash
    cd Terminal-TimeCapsule
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python timecapsule.py
    ```

## Usage

### Creating a Time Capsule

```bash
python timecapsule.py create -o "YYYY-MM-DD" -m "Your message"
```

### Listing Time Capsules

```bash
python timecapsule.py list
```

### Opening a Time Capsule

```bash
python timecapsule.py open "YYYY-MM-DD"
```

### Deleting a Time Capsule

```bash
python timecapsule.py delete "YYYY-MM-DD"
```

### Displaying Help

```bash
python timecapsule.py -h
```