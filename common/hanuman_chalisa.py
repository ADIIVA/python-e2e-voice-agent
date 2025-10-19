from typing import List, Dict


# Concise teaching set for Hanuman Chalisa (kid-friendly summaries)
# Each step includes a short title, the verse text (or excerpt),
# a simple translation, and an engagement prompt.

HANUMAN_CHALISA_STEPS: List[Dict[str, str]] = [
    {
        "title": "Doha 1",
        # "playback_audio_path": "/Users/admin/Desktop/projects/flask-agent-function-calling-demo/common/doha_1.mp3",
        "text_english": "Shree Guru Charan Saroj Raj, Nij mann mukur sudharee, Varnao Raghubar Vimal Jasu, Jo dayaku phal charee",
        "text_hindi": "श्रीगुरु चरन सरोज रज, निज मन मुकुर सुधारि। बरनउँ रघुबर बिमल जसु, जो दायकु फल चारि॥",
        "translation_hindi": "मैं अपने गुरुजी के कमल जैसे पैरों की धूल से अपने मन के आईने को साफ़ करता हूँ। फिर, मैं भगवान राम के गुण गाता हूँ । भगवान राम हमें धर्म, अर्थ, काम और मोक्ष — ये चारों फल देते हैं। ",
        "translation_english": "I clean my mind's mirror with the dust of my Guru's lotus feet. Then, I sing the sweet and pure glories of Lord Rama. He grants us four wishes, the wishes of happiness, success, love and peace",
        "learning_hindi": "अपने गुरु और बड़ों का सम्मान करें। उनकी बात ध्यान से सुनें, क्योंकि वे ही हमें सही रास्ता बताते हैं।",
        "learning_english": "Respect your teachers and elders. Listen carefully to them, as they always guide us on the right path in life.",
    },
    {
        "title": "Doha 2",
        # "playback_audio_path": "/Users/admin/Desktop/projects/flask-agent-function-calling-demo/common/doha_2.mp3",
        "text_english": "Buddhihin Tanu Jaanike, Sumirou Pavan kumar, Bal budhi Vidya dehu mohee, Harahu Kales Vikar",
        "text_hindi": "बुद्धिहीन तनु जानिके, सुमिरौं पवनकुमार। बल बुधि विद्या देहु मोहि, हरहु कलेस बिकार॥",
        "translation_hindi": "मैं जानता हूँ कि मैं अपनी बुद्धि (समझ और ज्ञान) में बहुत छोटा और कमजोर हूँ।इसलिए मैं पवन पुत्र हनुमान का स्मरण करता हूँ और उनसे मदद माँगता हूँ। हे हनुमान जी, मुझे शक्ति (बल), समझदारी (बुद्धि), और ज्ञान (विद्या) दो, ताकि मैं अच्छा कर सकूँ और भगवान राम की भक्ति सही ढंग से कर सकूँ।और मेरे सभी दुख, परेशानियाँ और बुरे विचार दूर करो।",
        "translation_english": "I know I'm small and not very smart. I pray to Hanumanji. Hanumanji, please give me strength, good sense, and knowledge, and take away all my sorrows and bad habits.",
        "learning_hindi": "हमेशा अच्छे विचार और शक्ति के लिए पूछें। दुख और बुरे विचार को दूर करने के लिए भगवान को पूछें और आपको सही चीज करने की आवश्यकता है।",
        "learning_english": "Always ask for good thoughts and strength. Pray to God to take away bad habits and give you the courage to do the right thing.",
    },
    {
        "title": "Chaupai 1",
        # "playback_audio_path": "/Us ers/admin/Desktop/projects/flask-agent-function-calling-demo/common/chaupai_1.mp3",
        "text_english": "Jai Hanuman gyan gun sagar, Jai Kapis tihun lok ujagar",
        "text_hindi": "जय हनुमान ज्ञान गुन सागर । जय कपीस तिहुँ लोक उजागर ॥ १ ॥",
        "translation_hindi": "हे हनुमान जी, आपकी जय हो! आप तो ज्ञान और अच्छे गुणों का बहुत बड़ा सागर हैं। हे वानरों के राजा, आपकी जय हो! आप तीनों लोकों (धरती, आकाश, पाताल) में मशहूर हैं!",
        "translation_english": "Victory to Hanuman Ji! You are a great ocean of wisdom and good qualities. Victory to the King of Monkeys! Your light shines in all three worlds (like Earth, Sky, and the world below)!",
        "learning_hindi": "समझदार और गुणी बनें। खूब पढ़ें और अच्छी आदतें (जैसे सच बोलना, शेयर करना) सीखें। अच्छे गुण आपको ज्ञानी बनाते हैं।",
        "learning_english": "Be wise and have good qualities. Study hard and adopt good habits (like telling the truth and sharing). Good qualities make you a knowledgeable person.",
    },
    {
        "title": "Chaupai 2",
        # "playback_audio_path": "/Users/admin/Desktop/projects/flask-agent-function-calling-demo/common/chaupai_2.mp3",
        "text_english": "Ram doot atulit bal dhama, Anjani-putra Pavan sut nama",
        "text_hindi": "राम दूत अतुलित बल धामा । अञ्जनि-पुत्र पवनसुत नामा ॥ २ ॥",
        "translation_hindi": "आप श्री राम जी के दूत (संदेशवाहक) हैं और आपके पास बहुत, बहुत ज़्यादा ताकत है। आप माता अंजनी के प्यारे बेटे और पवन देव (हवा के देवता) के पुत्र के नाम से भी जाने जाते हैं।",
        "translation_english": "You are Lord Rama's messenger and a house of limitless strength. You are also known as Mother Anjani’s son and the son of Pawan Dev (the Wind God).",
        "learning_hindi": "हमेशा अपने काम के लिए तैयार रहें। जैसे हनुमानजी रामजी के लिए, वैसे ही हमें अपने माता-पिता और टीचर के हर काम के लिए हमेशा 'हाँ' बोलना चाहिए।",
        "learning_english": "Always be ready to help. Just like Hanumanji was ready for Rama, always be ready to say 'yes' to your parents and teachers' tasks.",
    },
    {
        "title": "Chaupai 3",
        # "playback_audio_path": "/Users/admin/Desktop/projects/flask-agent-function-calling-demo/common/chaupai_3.mp3",
        "text_english": "Mahavir Vikram Bajrangi, Kumati nivar sumati Ke sangi",
        "text_hindi": "महाबीर बिक्रम बजरङ्गी । कुमति निवार सुमति के सङ्गी ॥ ३ ॥",
        "translation_hindi": "आप बहुत बहादुर हैं, और आपका शरीर वज्र (एक बहुत मज़बूत हथियार) की तरह मज़बूत है। आप बुरी अक्ल (कुमति) को दूर करते हैं और अच्छी अक्ल (सुमति) वालों के दोस्त हैं।",
        "translation_english": "You are a Great Hero (Mahavir), and your body is as strong as a thunderbolt (Vajra). You take away bad thoughts and are a friend to those with good sense.",
        "learning_hindi": "बुरी सोच को दूर भगाओ और अच्छे दोस्त बनाओ। गलत बातें सोचना छोड़ें और उन बच्चों से दोस्ती करें जो आपको खेलने और पढ़ने में मदद करते हैं।",
        "learning_english": "Chase away bad thoughts and choose good friends. Stop thinking mean things and make friends who help you play and study nicely.",
    },
    {
        "title": "Chaupai 4",
        # "playback_audio_path": "/Users/admin/Desktop/projects/flask-agent-function-calling-demo/common/chaupai_3.mp3",
        "text_english": "Kanchna Baran Bijar Ses, Kanan Kundal Kuncit Kesa",
        "text_hindi": "कञ्चन बरन बिराज सुबेसा । कानन कुण्डल कुञ्चित केसा ॥ ४ ॥",
        "translation_hindi": "आपका रंग सोने जैसा है, और आपने बहुत सुंदर कपड़े पहने हैं। आपके कानों में कुण्डल (बाली) हैं और आपके बाल घुंघराले हैं, जो बहुत प्यारे लगते हैं।",
        "translation_english": "Your body shines with a golden color, and you wear nice clothes. You have pretty earrings and lovely curly hair.",
        "learning_hindi": "हमेशा साफ़-सुथरा और व्यवस्थित दिखें। रोज नहाओ, साफ कपड़े पहनो और अपने बालों को कंघी करो। साफ-सफाई अच्छी आदत है।",
        "learning_english": " Always look clean and tidy. Bathe daily, wear clean clothes, and comb your hair. Being neat is a sign of good habits.",
    },
    {
        "title": "Chaupai 5",
        # "playback_audio_path": "/Users/admin/Desktop/projects/flask-agent-function-calling-demo/common/chaupai_3.mp3",
        "text_english": "Bijaya Baniketu Kama, Bijaya Baniketu Kama",
        "text_hindi": "हाथ बज्र औ ध्वजा बिराजै । काँधे मूँज जनेऊ साजै ॥ ५ ॥",
        "translation_hindi": "आपके एक हाथ में वज्र (गदा या एक तरह का हथियार) और दूसरे में झंडा (ध्वजा) है। आपके कंधे पर जनेऊ (एक पवित्र धागा) बहुत सुंदर लगता है।",
        "translation_english": "You hold a Mace (Vajra) and a Flag (Dhwaja) in your hands. A sacred thread called Janeu looks good on your shoulder.",
        "learning_hindi": "अपने इरादों में पक्के रहें। जब आप कोई लक्ष्य (जैसे कि एग्ज़ाम में अच्छा करना) बनाते हैं, तो उस पर एक झंडे की तरह पक्के रहें।",
        "learning_english": "Have firm intentions. When you set a goal (like doing well in an exam), stick to it like a flag planted firmly on the ground.",
    },
    
    
]


