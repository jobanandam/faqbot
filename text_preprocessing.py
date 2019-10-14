from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer

dictionary = []
stopword = list(stopwords.words('english'))
for i in range(0, 1000):
    stopword.append(str(i))
stopword.append('”')
stopword.append('&')
stopword.append('+')
stopword.append(')')
stopword.append('(')
stopword.append('?')
stopword.append('!')
stopword.append('>')
stopword.append('<')
stopword.append(':')
stopword.append(',')
stopword.append("'")
stopword.append("-")
stopword.append(".")
stopword.append("’")
stopword.append("'m")

sb = SnowballStemmer('english')
lemmatizer = WordNetLemmatizer()

questions = ["What is Apple Pay?",
"Is Apple Pay free?",
"Which payment cards can I add to Apple Pay? ",
"How do I activate Apple Pay in Hello bank! App?",
"How do I activate Apple Pay in Wallet?",
"How many payment cards can I add to Apple Pay?",
"Can I register a card on multiple devices in Apple Pay?",
"How do I change my default card?",
"How can I remove a card from Apple Pay?",
"Can I become a client if I live abroad? ",
"Can I become a client if I'm not Belgian?",
"Can I subscribe to Hello bank!’s or Hello4You’s bank offer as a legal entity?",
"Are there user fees for the Hello or Hello4You offer? ",
"Where do I find my contract?",
"What are the conditions to subscribe to the Hello offer?",
"What are the conditions to subscribe to the Hello4You offer?",
"Can I go to a BNP Paribas Fortis agency for advice?",
"I want to convert my BNP Paribas Fortis account into a Hello current account. What do I do?"]

answers = [
	"Apple Pay is Apple's payment service that allows you to pay more easily, faster and safer than ever for your purchases in shops, in apps and on websites in Safari with your iPhone, iPad, Apple Watch or Mac.",
"Yes, the Apple Pay service is free.",
"You can use Apple Pay with your debit card(s) and your credit card(s), issued by Hello bank!. The first card you add to Apple Pay will be your default card.",
"Apple Pay requires the latest version of iOS, watchOS or macOS on your device. For the iPhone, that is currently iOS 12.1. The Apple support website has more information on how to update your iPhone or IPad, Apple Watch or Mac.  For iPhone only:  Log into Hello bank! app on your iPhone and tap 'More' > 'Settings' > 'Apple Pay' > 'Get started'. An overview of your debit and credit cards will appear. Select the first card you want to use with Apple Pay and tap 'Add to Apple Wallet' > 'Next'. Read the general conditions and tap 'Agree' > 'Done'. The card is now ready for payments with Apple Pay on your iPhone.  For iPhone and Apple Watch:  Log into Hello bank! app on your iPhone and tap 'More' > 'Settings' > 'Apple Pay' > 'Get started'. An overview of your debit and credit cards will appear. Select the first card you want to use with Apple Pay and tap 'Add to Apple Wallet'. Select your iPhone and tap 'Next'. Read the general conditions and tap 'Agree' > 'Done'.  The card is now ready for payments with Apple Pay on your iPhone. Then tap 'Add to Apple Wallet' next to your Apple Watch and repeat the same steps: Choose card > 'Add to Apple Wallet' > 'Next' > 'Agree' > 'Done'. Apple Pay has now also been activated for payments with the chosen card on your Apple Watch.  For iPad:  You can't use Hello bank! app to activate Apple Pay on your iPad. You need to activate Apple Pay in 'Settings', as described below.",
"Apple Pay requires the latest version of iOS, watchOS or macOS on your device. For the iPhone, that is currently iOS 12.1. The Apple support website has more information on how to update your iPhone or iPad, Apple Watch or Mac.  For iPhone:  Open the Wallet app on your iPhone. Tap the '+' in the top right corner. Read the Apple Pay Privacy Policy and tap 'Continue'. Select Hello bank! and then the type of card you wish to add. When you add a debit card, you will automatically go to the Hello bank! login screen (or a screen where you can download the free app first). Once you have logged in, you will see an overview of your bank and credit cards. Select the first card you want to use with Apple Pay and tap 'Add to Apple Wallet' > 'Next'. Read the general conditions and tap 'Agree' > 'Done'. The card is now ready for payments with Apple Pay on your iPhone.  To add a credit card, you have to scan it, check the details and enter the security code (this is the CVC code on the back of your credit card). Then tap 'Next', read the general conditions and tap 'Agree'. Because you have not yet logged into your bank, you must now identify yourself to confirm that you are the rightful owner of the card. You can do this in three ways: with an SMS code, in Easy Banking App or by calling +32 (0)2 433 43 67. To complete the verification, tap 'Next'. The credit card is now ready for payments with Apple Pay on your iPhone.  For Apple Watch:  Open the Apple Watch app on your iPhone and tap 'My Watch'> 'Wallet & Apple Pay'> 'Add Card'. Enter your passcode on your Apple Watch to unlock it and tap 'Continue' on your iPhone. To add a credit card to Wallet on your Apple Watch, you have to scan it, check the details and enter the security code (this is the CVC code on the back of your credit card). For a debit card, you should enter the details manually. Then tap 'Next', read the general conditions and tap 'Agree'. Because you have not yet logged into your bank, you must now identify yourself to confirm that you are the rightful owner of the card. You can do this in three ways: with an SMS code, in Easy Banking App or by calling +32 (0)2 433 43 67. To complete the verification, tap 'Next'. The card is now ready for payments with Apple Pay on your Apple Watch.  For iPad:  The Wallet app is not available on your iPad. You should therefore add your cards to Wallet under 'Settings' > 'Wallet & Apple Pay' > 'Add Card'. On an iPad, you can only use Apple Pay with credit cards, not debit cards. To add a credit card, you have to scan it, check the details and enter the security code (this is the CVC code on the back of your credit card). Then tap 'Next', read the general conditions and tap 'Agree'. Because you have not yet logged into your bank, you must now identify yourself to confirm that you are the rightful owner of the card. You can do this in two ways: with an SMS code or by calling +32 (0)2 433 43 67. To complete the verification, tap 'Next'. The card is now ready for payments with Apple Pay on your iPad.  For MacBook Pro with Touch ID:  Go to 'System Preferences' > 'Wallet & Apple Pay' > 'Add Card'. On a Mac, you can only use Apple Pay with credit cards, not debit cards. To add a credit card, you need to enter your name, the card details and the security code (this is the CVC code on the back of your credit card). Then tap 'Next', read the general conditions and tap 'Agree'. Because you have not yet logged into your bank, you must now identify yourself to confirm that you are the rightful owner of the card. You can do this in two ways: with an SMS code or by calling +32 (0)2 433 43 67. To complete the verification, tap 'Next'. The card is now ready for payments with Apple Pay on your MacBook Pro with Touch ID.  For other Mac models:  To use Apple Pay with other Mac models, you need an Apple Pay-compatible iPhone or Apple Watch. Verify that you are logged in with the same Apple ID on both devices and that Bluetooth is enabled on your Mac. On your iPhone, go to 'Settings' > 'Wallet & Apple Pay' and enable the 'Allow Payments on Mac' option.",
"You can add up to 12 payment cards on iPhone 8, iPhone 8 Plus or later models and Apple Watch Series 3 or later models. You can add up to 8 payment cards on previous models.",
"Yes, you can.",
"The first card you add to Apple Pay will be your default card. If you have added more cards and you want to change your default card, follow the following steps:  iPhone:  Open the Wallet app. Hold your finger on the card you want to set as the new default card and drag it to the top of the card list.  iPad:  Go to 'Settings' > 'Wallet & Apple Pay'. Tap 'Default Card' and choose a new card.  Apple Watch:  Open the Apple Watch app on your iPhone. Tap on the tab 'My Watch' > 'Wallet & Apple Pay' > 'Default Card' and choose a new card.  MacBook Pro with Touch ID:  Go to 'System Preferences' > 'Wallet & Apple Pay'. Choose a new card from the 'Default Card' menu.",
"iPhone:  Open the Wallet app. Tap the card you want to remove and then the blue icon in the bottom right corner. On the next screen, scroll down and tap on 'Remove Card'.  iPad:  Go to 'Settings' > 'Wallet & Apple Pay'. Tap the card you want to remove and then on 'Remove Card'.  Apple Watch:  Open the Apple Watch app on your iPhone. Tap the 'My Watch' tab, scroll down and tap 'Wallet & Apple Pay'. Then tap the card you want to remove and on 'Remove Card'.",
"Only if you are still officially resident in Belgium. But don’t forget that your contracts, debit cards and other documents will reach your official address entered when you opened your account. ",
"Yes, of course. But you’ll have to live in Belgium and be the holder of a Belgian ID card*. There are exceptions for American citizens who cannot become clients. To fulfil American Tax Regulations (FATCA - Foreign Account Tax Compliance Act) and other guidelines concerning the bank account of American nationals or persons living in the United States, the bank cannot authorise a subscription to Hello bank!’s free offer.",
"Unfortunately not. Hello and Hello4You’s offers are only open to private individuals for private purposes.",
"Most transactions are free. Some uses of your current account and debit card must be paid, such as cash withdrawals in euro abroad outside the EU. For more information, please check the list of rates and general terms and conditions.",
"You’ve either received it by email. > You’ve received it by post.  If you’ve lost it, contact the Hello team from Monday to Friday (from 7 to 22) and Saturday (9 to 17) on +32 (0)2 433 41 45.",
"Be a physical person Be the holder of a Belgian ID CARD Be legally competent Be aged 28 years + Be two co-holders at most Main residence in Belgium",
"Be a physical person Be the holder of a Belgian ID CARD Be legally competent Be aged 18 years+ Be aged 27 years and nine month max. at the time of the opening of the account Be two co-holders at most, each being aged 18 years+ Be the holder of two Hello4You current accounts",
"Just like you, we’re mobile! But mobile doesn’t mean “no advice!”.  This is why Hello bank! gives its clients and members individual advice via the Hello team. The team of expert specialises in banking products and mobile technology. Contact the Hello team by phone from Monday to Friday (from 7 to 22) and Saturday (9 to 17) on +32 (0)2 433 41 45.  But Hello4You members can go to a BNP Paribas Fortis agency whenever they like.",
"It's very easy: Download the Hello bank! app. (available in the App Store and on Google Play). Click on “login”. Enter your BNP Paribas Fortis client number and your BNP Paribas Fortis card number. You can directly convert your BNP Paribas Fortis account into a Hello current account.",
]

for line in questions:
    line = line.lower()
    line = line.strip()
    tokens = word_tokenize(line)
    for each_token in tokens:
        if each_token not in stopword:
            each_token = sb.stem(each_token)
            each_token = lemmatizer.lemmatize(each_token)
            dictionary.append(each_token)

for line in answers:
    line = line.lower()
    line = line.strip()
    tokens = word_tokenize(line)
    for each_token in tokens:
        each_token = each_token.replace("“", "")
        each_token = each_token.replace("+", "")
        each_token = each_token.replace(".", "")
        each_token = each_token.replace("*", "")
        each_token = each_token.replace("'", "")
        each_token = each_token.strip()
        if each_token not in stopword:
            each_token = sb.stem(each_token)
            each_token = lemmatizer.lemmatize(each_token)
            dictionary.append(each_token)

dictionary = sorted(set(dictionary))
print(dictionary)

