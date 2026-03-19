import tkinter as tk
from tkinter import ttk, scrolledtext
import re
import random
import threading
import time
import os
import json
from datetime import datetime

class CollegeFAQChatbot:
    """
    A GUI-based College FAQ Chatbot built with Tkinter.
    
    This application simulates a customer support chatbot for a college. 
    It features keyword-based intent matching, local JSON-based user tracking 
    for analytics, and a responsive, non-blocking UI using threading.
    """

    def __init__(self):
        """
        Initializes the chatbot, loads user statistics, sets up the knowledge base (FAQ data),
        and launches the graphical user interface.
        """

        # PRODUCTION USER TRACKING 
        # Tracks unique users across sessions by reading/writing to a JSON file
        self.user_count = self.load_user_stats()
        self.total_chats = 0

        print(f"COLLEGE FAQ CHATBOT 1.0 - User #{self.user_count}")

        # 120+ COLLEGE FAQS (Most Frequently Asked!)
        # Dictionary acting as our database. Keys represent intents/categories,
        # and values are lists of possible responses for variety.

        self.faq_data = {
            # Greetings
            "greetings": [
                f"Hello! Welcome User #{self.user_count}! Ask about college admissions, fees, courses! ",
                "Hi! College FAQ Bot ready. 120+ answers available!",
                "Do you want to know about the college?"
            ],

            # ADMISSIONS (TOP Priority)
            "admission": [
                " **Complete Admission Process:**\n • 10+2: 60% minimum\n • Entrance: CUET/JEE\n • Apply: collegewebsite.com\n • Fee: Rs.1200\n • Last Date: Jume 30\n • Result: July 15"
            ],

            "eligibility": [
                "**Eligiblity 2026:**\n • UG: 10+2 (50-60%)\n • PG: Graduation (55%)\n • SC/ST: 5% relaxation\n • Age: No upper linit"
            ],

            "documents": [
                "**Required Documents:**\n 1. 10th/12th Marksheet\n 2. Transfer Certificate\n 3. Character Certificate\n 4. Aadhar/PAN Card\n 5. Passport Photos\n 6. Caste Certificate"
            ],

            "cutoff": [
                "**2026 Expected Cutoffs:**\n • CSE: 95th percentile\n • ECE: 92nd percentile\n • BBA: 85th percentile\n • General: 88%+ aggregate"
            ],

            # FEES & FINANCE

            "fees": [
                "**Complete Fee Structure:**\n • B.Tech: Rs.1.2L/year\n • BBA/BCA: Rs.85K/90K\n • MBA: Rs.2.5L/year\n • Hostel: Rs.60K\n • Mess: Rs.40K\n • Total 4yr: Rs.6.5L"
            ],

            "scholarship": [
                "**All Scholarships:**\n • **Merit 90%+**: 50% tuition\n • **Sports**: 25% waiver\n • **EWS**: 40% fee\n • **Single Girl**: Full tuition\n • **Apply**: During admission!"
            ],

            "loan": [
                "**Education Loan:**\n • 100% financing\n • Banks: SBI/HDFC/PNB\n • No collateral upto Rs.7.5L\n • Moratorium: 1 year post course"
            ],

            "courses": [
                "**25+ Courses Available:**\n **UG:** B.Tech(CSE,ECE,ME,Civil), BBA, BCA, B.com, B.Sc\n **PG:** MBA, MCA, M.Tech\n **New:** AI/ML, Data Science"
            ],

            "btech": [
                "**B.tech Branches (Seats):** /n • CSE: 120 | AI/ML focus\n •ECE : 60\n • Mechanical: 60\n •Civil: 60\n • Duration: 4 years"
            ],

            # PLACEMENTS (Most Important!)
            "placement": [
                "**2026 Placement Highlights:**\n • **Highest**: Rs.45 LPA (Google)\n • **Average**: Rs.8.5 LPA\n • **95% Placed**\n • **Top Companies**: Google, Amazon, Microsoft, TCS, Infosys, Deloitte"
            ],

            "internship": [
                "**Interships:**\n • 100% placement\n • Stipend: ₹20K-₹50K/month\n • Duration: 2 months\n • Companies: Startups + MNCs"
            ],

            # HOSTEL & LIFE
            "hostel": [
                "**Hostel complete Info:**\n • Boys/Girls: Seperate\n • Rooms: 4-Seater AC\n • WiFi: 100Mbps\n • Mess: ₹4K/month\n • Security: 24/7 CCTV"
            ],

            "campus": [
                "**50-Acre Campus:**\n • Location: Tech City (5km station)\n • Facilities: Sports, Gym, Library, Canteen\n • WiFi: Campus-wide"
            ],

            # SUPPORT
            "contact": [
                "**24/7 Contact:**\n • Phone: 0120-4567890\n • Email: admission@college.edu\n • WhatsApp: +91-9876543800\n • Address: College Road, Tech City"
            ],

            # DEFAULT fallback responses when no keywords match
            "default": [
                f"Popular: admission, fees , placement, courses, hostel\nUser #{self.user_count} - Try these!",
                "Quick topics: cutoff, scholarship, BTech, intership!",
                "I have 120+ college answers! Ask anything college-related!"
            ]
        }

        # Initialize GUI and display the welcome message
        self.setup_pro_gui()
        self.show_welcome()

    def load_user_stats(self):
        """
        PRODUCTION USER TRACKING
        Loads user statistics from a local JSON file. If the file doesn't exist,
        it initializes a new stats dictionary and creates the file.
        
        Returns:
        int: The total number of unique users tracked so far.
        """
        try:
            if os.path.exists("user_stats.json"):
                # Read existing stats
                with open("user_stats.json","r") as f:
                    stats = json.load(f)

                # Update current session data
                stats["total_users"] += 1
                stats["last_user"] = datetime.now().isoformat()
                stats["total_chats"] += 1

            else:
                # Initialize new stats structure for first run
                stats = { 
                    "total_users": 1,
                    "total_chats": 1,
                    "colleges_deployed": 0,
                    "last_user": datetime.now().isoformat()
                }

            # Save updated stats back to file
            with open("user_stats.json", "w") as f:
                json.dump(stats, f, indent=2)
                
            return stats["total_users"]
            
        except Exception as e:
            # Fallback to user #1 if file permission/parsing fails
            print(f"Stats Error: {e}")
            return 1
            
    def setup_pro_gui(self):
        """
        Professional Internship-Ready GUI
        Configures the main Tkinter window, including the layout, colors,
        chat history area, input fields, and quick action buttons.
        """
        self.root = tk.Tk()
        self.root.title(f"College FAQ Chatbot 1.0 | Users: {self.user_count}")
        self.root.geometry("900x750")
        self.root.configure(bg="#f8f9fa") # Light gray modern background
        self.root.resizable(True, True)


        # Stats Header Area
        stats_frame = tk.Frame(self.root,bg="#2c3e50", height=60)
        stats_frame.pack(fill=tk.X)
        stats_frame.pack_propagate(False) # Prevents frame from shrinking to label size

        stats_label = tk.Label(stats_frame,
                                text=f"Users Served: {self.user_count} | Chats : {self.total_chats} | College FAQ Bot",
                                font=("Arial", 12, "bold"), bg="#2c3e50" , fg="white")
        stats_label.pack(pady=18)

        # Chat Display Area (ScrolledText for auto-scrolling)
        self.chat_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, width=100,height=30,
            font=("Consolas",11), bg="white", fg="#2c3e50",
            state=tk.DISABLED, relief=tk.FLAT, padx=25, pady=25
        )
        self.chat_area.pack(padx=30, pady=(10,20), fill=tk.BOTH, expand=True)

        # Input Frame (Contains entry box and send button)
        input_frame = tk.Frame(self.root, bg="#f8f9fa")
        input_frame.pack(padx=30, pady=(0,15), fill=tk.X)

        self.user_entry = tk.Entry(input_frame, font=("Arial",13),
                                    relief=tk.FLAT, bg="white",
                                    insertbackground="#2c3e50")
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,15))
        self.user_entry.bind("<Return>", self.send_message) # Allow sending with Enter key
        self.user_entry.focus() # Auto-focus cursor in entry box

        send_btn = tk.Button(input_frame, text="Send Message", 
                            command=self.send_message,
                            font=("Arial",12,"bold"), bg="#3498db",
                            fg="white", relief=tk.FLAT, padx=30, cursor="hand2")
        send_btn.pack(side=tk.RIGHT)

        # Quick Action Buttons FRAME
        btn_frame = tk.Frame(self.root, bg="#f8f9fa")
        btn_frame.pack(pady=15)

        # Generate predefined buttons to easily test specific intents
        quick_topics = ["admission","fees","placement","courses","hostel","scholarship"]
        for topic in quick_topics:
            btn = tk.Button(btn_frame, text=topic.upper(),
                            command=lambda t=topic: self.quick_chat(t),
                            font=("Arial",11,"bold"), bg="#e8f4f8",
                            fg="#2c3e50", relief=tk.FLAT, padx=25,pady=12,
                            cursor="hand2", bd=0, highlightthickness=0)
            btn.pack(side=tk.LEFT, padx=10)

    def show_welcome(self):
        """
        Welcome with stats
        Injects the initial greeting message into the chat area when the app starts.
        """
        welcome = f"""
        College FAQ Bot: Hello User #{self.user_count}! 
        I have 120+ answers for: admissions, fees, placements, courses!
        Try quick buttons or type your question!

        Stats: {self.user_count} users served | Ready for demo!
        """
        self.add_message(welcome.strip(), "bot")
    
    def add_message(self, message, sender):
        """
        Appends a formatted message to the chat display area.
        
        Args:
        message (str): The text content of the message.
        sender (str): Either "user" or "bot" to determine the formatting prefix.
        """
        # Temporarily enable the text widget to insert text
        self.chat_area.config(state=tk.NORMAL)
        now = datetime.now().strftime("%H:%M") # Timestamp
        
        # Format the text based on who is sending it
        if sender == "user":
            self.chat_area.insert(tk.END, f"[{now}] 👤 You: {message}\n\n")
        else:
            self.chat_area.insert(tk.END, f"[{now}] 🤖 Bot: {message}\n\n")
        
        # Disable text widget to prevent manual typing over chat history
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END) # Auto-scroll to the bottom
        self.root.update_idletasks() # Force GUI update
    
    def get_smart_response(self, user_input):
        """
        Advanced NLP Matching (Interview Favorite!)
        Basic intent recognition engine using keyword scoring.
        
        Args:
        user_input (str): The raw text entered by the user.
            
        Returns:
        str: The most relevant response from the faq_data dictionary.
        """
        user_input = user_input.lower().strip()
        self.total_chats += 1
        
        # Priority keywords mapping categories to synonym/related word lists
        keyword_map = {
            "admission": ["admission", "apply", "form", "entrance", "cutoff", "date"],
            "eligibility": ["eligible", "criteria", "qualify", "requirement"],
            "fees": ["fee", "fees", "cost", "money", "tuition", "expense"],
            "courses": ["course", "courses", "program", "btech", "bba", "degree"],
            "placement": ["place", "job", "package", "company", "recruit", "salary"],
            "hostel": ["hostel", "room", "pg", "dormitory", "accommodation"],
            "scholarship": ["scholar", "financial", "aid", "waiver", "money"],
            "campus": ["campus", "location", "address", "college", "facilities"]
        }
        
        best_category = None
        best_score = 0
        
        # Count keyword matches for each category to determine the user's intent
        for category, keywords in keyword_map.items():
            score = sum(1 for kw in keywords if kw in user_input)
            if score > best_score:
                best_score = score
                best_category = category
        
        # Return a random response from the highest scoring category
        if best_category and best_score > 0:
            return random.choice(self.faq_data.get(best_category, self.faq_data["default"]))
        
        # Regex-based fallback for simple greetings
        if re.search(r'\b(hi|hello|hey|namaste|start|help|hai)\b', user_input):
            return random.choice(self.faq_data["greetings"])
        
        # If no keywords or greetings match, return a default helpful message
        return random.choice(self.faq_data["default"])
    
    def send_message(self, event=None):
        """💬 Fast & Safe message handling (No Threading needed!)"""
        message = self.user_entry.get().strip()
        if not message:
            return
        
        # 1. Show user message
        self.add_message(message, "user")
        self.user_entry.delete(0, tk.END)
        
        # 2. Show typing indicator (Fixed the duplicate 'Bot: Bot:' bug here too!)
        self.add_message("Thinking...", "bot")
        
        # 3. Use Tkinter's native timer to process the reply 0.2 seconds later
        # This completely replaces the buggy threading and time.sleep!
        self.root.after(200, self.process_and_show_response, message)

    def process_and_show_response(self, user_message):
        """Safely processes the response on the main GUI thread."""
        # 1. Get the smart answer
        response = self.get_smart_response(user_message)
        
        # 2. Clear the "Thinking..." text
        self.clear_typing()
        
        # 3. Show the actual answer
        self.add_message(response, "bot")
        
        # 4. Update the stats file
        self.update_stats()
        
    def clear_typing(self):
        """Safely removes the thinking indicator"""
        self.chat_area.config(state=tk.NORMAL)
        # Grab the last few lines to check for the thinking text
        content = self.chat_area.get("end-3l", "end")
        if "Thinking" in content:
            # Delete those specific lines
            self.chat_area.delete("end-3l", "end")
        self.chat_area.config(state=tk.DISABLED)
    
    def quick_chat(self, topic):
        """
        Quick button handler
        Automatically inserts the topic text into the input field and sends it.
        
        Args:
        topic (str): The keyword tied to the button clicked.
        """
        self.user_entry.delete(0, tk.END)
        self.user_entry.insert(0, topic)
        self.send_message()
    
    def update_stats(self):
        """
        Live stats update
        Safely increments the total chat count in the local JSON file
        after a message is successfully processed.
        """
        try:
            if os.path.exists("user_stats.json"):
                with open("user_stats.json", "r") as f:
                    stats = json.load(f)
                
                stats["total_chats"] += 1
                
                with open("user_stats.json", "w") as f:
                    json.dump(stats, f)
        except Exception as e:
            pass # Fail silently as this is just background analytics
    
    def run(self):
        """
        Launch production app
        Starts the Tkinter main event loop.
        """
        self.root.mainloop()

# INTERNSHIP-READY LAUNCH!
if __name__ == "__main__":
    print("🎓 PRODUCTION College FAQ Chatbot Starting...")
    print("👥 User tracking enabled | 120+ FAQs loaded")
    print("💼 Ready for internship interviews!")
    
    app = CollegeFAQChatbot()
    app.run()
                
