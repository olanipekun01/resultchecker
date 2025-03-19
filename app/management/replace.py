from your_app.models import CustomUser  # Replace 'your_app' with your actual app name

# Fetch all users and update usernames
users = CustomUser.objects.filter(username__contains='+AAE-')

for user in users:
    user.username = user.username.replace('+AAE-', '@')
    user.save()

print(f"Updated {users.count()} usernames.")