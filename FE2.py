import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.ttk as ttk

# Database setup
engine = create_engine('sqlite:///election.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define database tables
class Voter(Base):
    __tablename__ = 'voter'
    id = Column(Integer, primary_key=True)
    account = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    has_voted = Column(Boolean, default=False)
    site = Column(String, nullable=True)  # Change site column type to String
    age = Column(Integer, nullable=True)  # Add age column


class Vote(Base):
    __tablename__ = 'vote'
    id = Column(Integer, primary_key=True)
    voter_id = Column(Integer, ForeignKey('voter.id'), nullable=False)
    candidate_id = Column(Integer, ForeignKey('candidate.id'), nullable=False)
    voter = relationship('Voter')
    candidate = relationship('Candidate')

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    account = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Candidate(Base):
    __tablename__ = 'candidate'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    party = Column(String, nullable=False)

# Create database tables
Base.metadata.create_all(engine)

# Check if candidates exist in the database, if not, add them
candidates_info = [
    {"name": "Kennedy", "party": "Party A"},
    {"name": "Biden", "party": "Party B"},
    {"name": "Trump", "party": "Party C"},
    {"name": "Putin", "party": "Party D"},
    {"name": "Macron", "party": "Party E"}
]

existing_candidate_names = [candidate.name for candidate in session.query(Candidate).all()]

for data in candidates_info:
    if data["name"] not in existing_candidate_names:
        candidate = Candidate(name=data["name"], party=data["party"] )
        session.add(candidate)

    # Add preset voter information
pre_defined_voters_info = [
        {"account": "a1", "password": "1", "age": 25, "has_voted": False, "site": 1},
        {"account": "b2", "password": "2", "age": 30, "has_voted": False, "site": 2},
        {"account": "c3", "password": "3", "age": 22, "has_voted": False, "site": 3},
        {"account": "d4", "password": "4", "age": 25, "has_voted": False, "site": 5},
        {"account": "e5", "password": "5", "age": 25, "has_voted": False, "site": 1},
        {"account": "f6", "password": "6", "age": 34, "has_voted": False, "site": 2},
        {"account": "g7", "password": "7", "age": 45, "has_voted": False, "site": 4},
        {"account": "h8", "password": "8", "age": 25, "has_voted": False, "site": 1},
        {"account": "i9", "password": "9", "age": 36, "has_voted": False, "site": 7},
        {"account": "j10", "password": "10", "age": 30, "has_voted": False, "site": 8},
        {"account": "k11", "password": "11", "age": 31, "has_voted": False, "site": 1},
        {"account": "l12", "password": "12", "age": 27, "has_voted": False, "site": 1},
        {"account": "m13", "password": "13", "age": 28, "has_voted": False, "site": 3},
        {"account": "n14", "password": "14", "age": 29, "has_voted": False, "site": 6},
        {"account": "015", "password": "15", "age": 36, "has_voted": False, "site": 6}

    ]

for data in pre_defined_voters_info:
    existing_voter = session.query(Voter).filter_by(account=data["account"]).first()
    if existing_voter:
        # If the same account name already exists, the current loop is skipped without the insertion
        continue

    voter = Voter(account=data["account"], password=data["password"], age=data["age"], has_voted=data["has_voted"],
                  site=data["site"])
    session.add(voter)


session.commit()

# Predefined admin account
admin_account = "admin"
admin_password = "admin"

# GUI setup
class ElectionSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Election System")
        self.logged_in_user = None  # Store the logged-in user's account here
        self.site_map = {"Site 1": 1, "Site 2": 2, "Site 3": 3, "Site 4": 4, "Site 5": 5, "Site 6": 6, "Site 7": 7,
                         "Site 8": 8}  # Mapping of site strings to integers
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="account:").grid(row=0, column=0)
        tk.Label(self.root, text="Password:").grid(row=1, column=0)

        # Adding a prompt
        tk.Label(self.root, text="If you have any questions, please contact 4008-823-823").grid(row=4, column=0,
                                                                                                columnspan=2)

        total_registered = session.query(func.count(Voter.id)).scalar()
        total_voted = session.query(func.count(Voter.id)).filter_by(has_voted=True).scalar()
        total_not_voted = total_registered - total_voted
        # Shows the number of registrations and votes cast
        tk.Label(self.root, text=f"Total registered: {total_registered}").grid(row=2, column=0, columnspan=2)
        tk.Label(self.root, text=f"Total voted: {total_voted}").grid(row=3, column=0, columnspan=2)
        # Create a pie chart
        labels = ['Voted', 'Not Voted']
        sizes = [total_voted, total_not_voted]
        fig, ax = plt.subplots(figsize=(2, 2))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)  # Resize the pie chart

        # Display the pie chart on the login screen
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=7, column=0, columnspan=2)

        self.account_entry = tk.Entry(self.root)
        self.password_entry = tk.Entry(self.root, show='*')
        self.account_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        tk.Button(self.root, text="Login", command=self.login).grid(row=5, column=0, columnspan=2)
        tk.Button(self.root, text="Register", command=self.create_register_screen).grid(row=6, column=0, columnspan=2)

    def create_register_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="account:").grid(row=0, column=0)
        tk.Label(self.root, text="Password:").grid(row=1, column=0)
        tk.Label(self.root, text="Age:").grid(row=2, column=0)  # Add an age tag
        tk.Label(self.root, text="Site:").grid(row=3, column=0)  # Adds a label for the site selection
        self.account_entry = tk.Entry(self.root)
        self.password_entry = tk.Entry(self.root, show='*')
        self.age_entry = tk.Entry(self.root)  # Add an age field
        self.site_combobox = ttk.Combobox(self.root, values=list(self.site_map.keys()))  # int
        self.account_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        self.age_entry.grid(row=2, column=1)  # Displays the age field
        self.site_combobox.grid(row=3, column=1)  # Displays a drop-down menu for site selection
        tk.Button(self.root, text="Register", command=self.register).grid(row=4, column=0, columnspan=2)

    def create_vote_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Vote Eligibility:").grid(row=0, column=0, columnspan=2)
        if not self.logged_in_user or not isinstance(self.logged_in_user, Voter):
            tk.Label(self.root, text="You are not logged in as a voter.").grid(row=1, column=0, columnspan=2)
        elif self.logged_in_user.has_voted:
            tk.Label(self.root, text="You have already voted.").grid(row=1, column=0, columnspan=2)
        else:
            tk.Label(self.root, text="You are eligible to vote.").grid(row=1, column=0, columnspan=2)

        tk.Label(self.root, text="Select Candidate:").grid(row=2, column=0)

        candidates = session.query(Candidate).all()
        self.selected_candidate_id = tk.IntVar()
        row = 3
        for candidate in candidates:
            tk.Radiobutton(self.root, text=f"{candidate.name} - {candidate.party}", variable=self.selected_candidate_id,
                           value=candidate.id).grid(
                row=row, column=0, sticky=tk.W)
            row += 1

        tk.Button(self.root, text="Vote", command=self.vote).grid(row=row, column=0, columnspan=2)

    def create_results_screen(self):
        self.clear_screen()
        votes = session.query(Vote.candidate_id, func.count(Vote.candidate_id)).group_by(Vote.candidate_id).all()
        candidate_names = []
        vote_counts = []

        for candidate_id, count in votes:
            candidate = session.query(Candidate).filter_by(id=candidate_id).first()
            candidate_names.append(candidate.name)
            vote_counts.append(count)

        fig, ax = plt.subplots()
        ax.bar(candidate_names, vote_counts)
        ax.set_ylabel('Votes')
        ax.set_xlabel('Candidates')
        ax.set_title('Election Results')

        # Convert Matplotlib figure to Tkinter compatible format
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def login(self):
        account = self.account_entry.get()
        password = self.password_entry.get()
        if account == admin_account and password == admin_password:
            # If the account name and password you entered match the default administrator account name and password
            messagebox.showinfo("Welcome", "Welcome back, administrator")
            self.create_admin_dashboard_screen()
            return
        # If it is not an administrator account, proceed to check the records in the database
        user = session.query(Voter).filter_by(account=account).first() or session.query(Admin).filter_by(
            account=account).first()
        if user and user.password == password:
            self.logged_in_user = user
            if isinstance(user, Voter):
                self.create_vote_screen()
            else:
                self.create_admin_dashboard_screen()
        else:
            messagebox.showerror("Login Error", "Invalid account or password")

    def register(self):
        account = self.account_entry.get()
        password = self.password_entry.get()
        age_str = self.age_entry.get()  # Gets the age entered by the user

        # Check that the age matches the format
        age_is_valid = age_str.isdigit()
        if not age_is_valid:
            messagebox.showerror("Registration Error", "Age must be a valid integer.")
            return

        age = int(age_str)

        # Check if the age is under 18
        if age < 18:
            messagebox.showerror("Registration Error", "You must be 18 years or older to register.")
            return
        # Gets the site selected by the user and converts to an integer value
        site = self.site_map[self.site_combobox.get()]
        # Add site and age information to the newly registered voter object
        new_voter = Voter(account=account, password=password, site=site, age=age)
        session.add(new_voter)
        session.commit()
        messagebox.showinfo("Registration Success", "Registration Success")
        self.create_login_screen()

    def vote(self):
        candidate_id = self.selected_candidate_id.get()

        # Checks if the user has voted
        if self.logged_in_user and isinstance(self.logged_in_user, Voter) and not self.logged_in_user.has_voted:
            # Record the vote
            new_vote = Vote(voter_id=self.logged_in_user.id, candidate_id=candidate_id)
            self.logged_in_user.has_voted = True
            session.add(new_vote)
            session.commit()
            messagebox.showinfo("Vote Success", "Vote Success")
            self.create_results_screen()  # Results are displayed after voting
        else:
            messagebox.showerror("Vote Error", "You have already voted")

    def create_admin_dashboard_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="administrator", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2)

        # Shows the current voting results
        self.show_current_results()

        # Add a bar chart of the current poll results
        self.show_current_results_bar_chart()

        # Add a bar chart of the site distribution and a pie chart of the percentage of people who have voted
        self.show_site_distribution_bar_and_vote_pie_chart()

        # The Add button is used to create new users
        tk.Button(self.root, text="Create New User", command=self.create_register_screen).grid(row=0, column=2)
        # Add a button to update the user
        tk.Button(self.root, text="Update User Profile", command=self.update_user_profile).grid(row=0, column=3)

        # Add a button to view voting records
        tk.Button(self.root, text="View Vote Records", command=self.show_vote_records).grid(row=0, column=4)

    def show_vote_records(self):
        self.vote_records_window = tk.Toplevel(self.root)
        self.vote_records_window.title("Vote Records")

        tk.Label(self.vote_records_window, text="Vote Records", font=("Helvetica", 16)).grid(row=0, column=0,
                                                                                             columnspan=2)

        votes = session.query(Vote).all()

        row = 1
        for vote in votes:
            voter_initial = vote.voter.account[0] + '*' * (len(vote.voter.account) - 1)
            candidate_initial = vote.candidate.name[0] + '*' * (len(vote.candidate.name) - 1)
            tk.Label(self.vote_records_window, text=f"{voter_initial} voted for {candidate_initial}").grid(row=row,
                                                                                                           column=0,
                                                                                                           columnspan=2)
            row += 1

        tk.Button(self.vote_records_window, text="Close", command=self.vote_records_window.destroy).grid(row=row,
                                                                                                         column=0,
                                                                                                         columnspan=2)

    def update_user_profile(self):
        self.clear_screen()
        tk.Label(self.root, text="Update User Profile", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2)

        tk.Label(self.root, text="Enter User Account:").grid(row=1, column=0)
        self.user_account_entry = tk.Entry(self.root)
        self.user_account_entry.grid(row=1, column=1)

        tk.Label(self.root, text="New Password:").grid(row=2, column=0)
        self.new_password_entry = tk.Entry(self.root, show='*')
        self.new_password_entry.grid(row=2, column=1)

        tk.Label(self.root, text="New Age:").grid(row=3, column=0)
        self.new_age_entry = tk.Entry(self.root)
        self.new_age_entry.grid(row=3, column=1)

        tk.Button(self.root, text="Update Profile", command=self.perform_update).grid(row=4, column=0, columnspan=2)

    def perform_update(self):
        user_account = self.user_account_entry.get()
        new_password = self.new_password_entry.get()
        new_age_str = self.new_age_entry.get()

        # Check if the user exists
        user = session.query(Voter).filter_by(account=user_account).first()
        if user:
            # Update the user's password
            if new_password:
                user.password = new_password

            # Update the user's age
            if new_age_str:
                new_age = int(new_age_str)
                if new_age >= 18:
                    user.age = new_age
                else:
                    messagebox.showerror("Update Error", "Age must be 18 or older.")
                    return

            # Commit the changes to the database
            session.commit()
            messagebox.showinfo("Update Success", "User profile updated successfully.")
            self.create_admin_dashboard_screen()  # Return to the administrator screen
        else:
            messagebox.showerror("Update Error", "User not found.")


    def show_current_results_bar_chart(self):
        votes = session.query(Vote.candidate_id, func.count(Vote.candidate_id)).group_by(Vote.candidate_id).all()
        candidates = [session.query(Candidate).filter_by(id=candidate_id).first() for candidate_id, _ in votes]
        vote_counts = [count for _, count in votes]

        fig, ax = plt.subplots(figsize=(3, 3))
        ax.bar([candidate.name for candidate in candidates], vote_counts)
        ax.set_ylabel('Votes')
        ax.set_xlabel('Candidates')
        ax.set_title('Election Results')

        # Convert Matplotlib graphs to a Tkinter compatible format
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def show_site_distribution_bar_and_vote_pie_chart(self):
        sites = session.query(Voter.site, func.count(Voter.id)).group_by(Voter.site).all()

        fig, ax = plt.subplots(figsize=(3, 3))
        ax.bar([f"site {site}" for site, _ in sites], [count for _, count in sites])
        ax.set_ylabel('Number of voters')
        ax.set_xlabel('Site')
        ax.set_title('Site distribution')

        # Convert Matplotlib figure to Tkinter compatible format
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=12, column=0, columnspan=2, padx=10, pady=10)  # Adjusted grid parameters

        # Plot the pie chart for the vote percentage
        total_registered = session.query(func.count(Voter.id)).scalar()
        total_voted = session.query(func.count(Voter.id)).filter_by(has_voted=True).scalar()
        total_not_voted = total_registered - total_voted
        labels = ['Voted', 'Not Voted']
        sizes = [total_voted, total_not_voted]

        # Check if any size is zero
        if any(size == 0 for size in sizes):
            # If any size is zero, set all sizes to 1
            sizes = [1] * len(sizes)

        # Check if all sizes are zero
        if all(size == 0 for size in sizes):
            # If all sizes are zero, set all sizes to equal values
            sizes = [1] * len(sizes)

        fig2, ax2 = plt.subplots(figsize=(3, 3))
        ax2.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax2.axis('equal')  # Ensure the pie chart is circular

        # Convert Matplotlib figure to Tkinter compatible format
        canvas2 = FigureCanvasTkAgg(fig2, master=self.root)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=12, column=8, columnspan=2, padx=10, pady=10)  # Adjusted grid parameters

    def show_current_results(self):
        tk.Label(self.root, text="Current Results", font=("Helvetica", 12)).grid(row=1, column=0, columnspan=2)

        votes = session.query(Vote.candidate_id, func.count(Vote.candidate_id)).group_by(Vote.candidate_id).all()
        candidates = [session.query(Candidate).filter_by(id=candidate_id).first() for candidate_id, _ in votes]
        vote_counts = [count for _, count in votes]

        for i, candidate in enumerate(candidates):
            tk.Label(self.root, text=f"{candidate.name}: {vote_counts[i]} votes").grid(row=i + 2, column=0, sticky=tk.W)



    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = ElectionSystem(root)
    root.mainloop()


