from collections import Counter
import re
import pytesseract
from PIL import Image
import csv
import matplotlib.pyplot as plt

def process_vote_images(image_paths):
    results = []
    #Load the Image
    for image_path in image_paths:
        img = Image.open(image_path)

        # Use tesseract to do OCR on the image
        text = pytesseract.image_to_string(img).strip()

        # Extract vote information using regular expressions
        candidate_match = re.search(r"Candidate\s([A-D])", text)
        sequence_match = re.search(r"(\d+)$", text, re.MULTILINE)

        candidate_letter = candidate_match.group(1) if candidate_match else 'Rejected'
        sequence_number = int(sequence_match.group(1)) if sequence_match else None

        results.append((candidate_letter, sequence_number))
    
    # Sort the results by sequence number, placing None values at the end
    sorted_results = sorted(results, key=lambda x: (x[1] is None, x[1]))

    # Verify sequence numbers are consecutive; if not, mark as rejected
    verified_results = []
    for i in range(len(sorted_results)):
        if i > 0 and sorted_results[i][1] is not None and sorted_results[i-1][1] is not None:
            if sorted_results[i][1] - sorted_results[i-1][1] != 1:
                verified_results.append(('Rejected', sorted_results[i][1]))
            else:
                verified_results.append(sorted_results[i])
        else:
            verified_results.append(sorted_results[i])
    return verified_results

#Extract the results into CSV file
def generate_results_csv(candidate_counts, total_votes):
    with open('election_results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Candidate', 'Votes', 'Percentage'])
        for candidate, count in candidate_counts.items():
            percentage = (count / total_votes) * 100 if total_votes > 0 else 0
            candidate_name = f"Candidate {candidate}" if candidate != 'Rejected' else candidate
            writer.writerow([candidate_name, count, f"{percentage:.2f}%"])
        writer.writerow(['Total Votes', total_votes, '100%'])

#Display Results Garaphcially
def plot_results(candidate_counts, total_votes):
    candidates = ['A', 'B', 'C', 'D', 'Rejected']
    votes = [candidate_counts.get(candidate, 0) for candidate in candidates]
    percentages = [(count / total_votes) * 100 if total_votes > 0 else 0 for count in votes]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(candidates, percentages, color=['red', 'green', 'blue', 'cyan', 'magenta'])

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom')

    plt.xlabel('Candidates and Rejected')
    plt.ylabel('Percentage')
    plt.title('Election Results')
    plt.ylim(0, max(percentages) + 10) 
    plt.show()

# Example image paths
image_paths = ['images/opencv_frame_0.png',
    'images/opencv_frame_1.png', 
    'images/opencv_frame_2.png',
    'images/opencv_frame_3.png', 
    'images/opencv_frame_4.png',
    'images/opencv_frame_5.png',
    'images/opencv_frame_6.png', 
    'images/opencv_frame_7.png',
    'images/opencv_frame_8.png', 
    'images/opencv_frame_9.png',
    'images/opencv_frame_10.png', 
    'images/opencv_frame_11.png',
    'images/opencv_frame_12.png'
    ]
verified_results = process_vote_images(image_paths)
candidate_counts = Counter(candidate for candidate, sequence in verified_results)
total_votes = sum(vote for candidate, vote in candidate_counts.items() if candidate != 'Rejected')


generate_results_csv(candidate_counts, total_votes)


plot_results(candidate_counts, total_votes)
