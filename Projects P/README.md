# 🏛️ Great Library of Alexandria - Library Management System

![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

This is a command-line library management system inspired by the ancient Library of Alexandria, designed to preserve knowledge against digital oblivion. This system allows you to catalog your personal book collection, manage users, track loans, and safeguard literary heritage. 

```bash
## Key features 
* 📚 Book Cataloging - Add books with full metadata
*👥 User Management - Register users with membership types
*🔄 Loan Tracking - Manage book borrowing and returns
*🔍 Advanced Search - Find books by multiple criteria
*💾 Data Persistence - Automatic saving to JSON
*📜 Transaction History - Full audit trail of operations
*🏺 Thematic Interface - Alexandrian library theme

## Quick start

git clone https://github.com/JuanEPastor/very-first-repo.git
cd very-first-repo

python library_v4.py


### Core Classes 
# Class         #Purpose
*Book           Represents books in your collection 
*User           Manages library system
*Library        Main system with all operations

###Data Storage 
*All data saves automatically to library_Alexandria.json:

    {
      "books": [
        {
         "id": 55,
         "title": "Las desventajas del Joven Werther",
         "author": "Goethe, Johann Wolfgang Von",
         "isbn": "9788437604077",
         "publisher_house": "CATEDRA",
         "year": "2005",
         "quantity": 1,
         "available": 1
        }
      ],
      "users": [],
      "transactions":[]
    }

###Basic Usage 
#Add a book
Select: 1
Title: The Master and Margarita
Author: Mikhail Bulgakov
ISBN: 9781419756504
Year: 1967
Copies: 1

#Borrow a book
Select: 4
User ID: 1
Book ID: 1

#Search books:
Select: 3 → 2 (By Author)
Author: Goethe

📜 License
MIT Licensed - See LICENSE for details.


