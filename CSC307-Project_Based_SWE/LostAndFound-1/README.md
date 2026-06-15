# LostAndFound
Lost and Found project repository

## Our Icons

[React icons github](https://react-icons.github.io/react-icons/)

## WHAT SHOULD BE IN YOUR .ENV
DATABASE_URL="postgresql://*user*:*password*@localhost:5432/*mydatabase*"
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_ZXhvdGljLWthdHlkaWQtNjkuY2xlcmsuYWNjb3VudHMuZGV2JA
CLERK_SECRET_KEY=sk_test_NFNLRyB3eLyjLfP1db3eoCwp9LznKDEJItHivyMKEH

NEXT_PUBLIC_CLERK_SIGN_IN_URL=/login_page

STREAM_API_SECRET=cw74q4x95vta49zbuymyb4gthnta9za7xz7nkuep8fsa26hxfcqdzfny6fre6r8b
NEXT_PUBLIC_STREAM_API_KEY=kv9ykmq8hgtn

## Usage
After forking from the repository and changing to its directory...
1. add the variables above to your `.env`
2. type `npm install` to your terminal
3. type `npx prisma migrate dev` to your terminal
4. type `npx prisma migrate reset` to your terminal

*[NOTE] to access the rest of the site's features, you need to sign up for a clerk account*
*[NOTE] in the .env you may need to change "user" "password" and "mydatabase" in your `DATABASE_URL`*
