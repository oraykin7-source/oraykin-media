# oraykin-media

תמונות מוכנות לפרסום ומטה העבודה של חשבון האינסטגרם @oraykin. ההוראות לצוות הסוכנים ב-`CLAUDE.md`, המצב העדכני ב-`docs/STATUS.md`.

## פתיחה במק (פעם ראשונה)
```bash
mkdir -p ~/Documents/Projects && cd ~/Documents/Projects
git clone https://github.com/oraykin7-source/oraykin-media.git
cd oraykin-media
pip3 install pillow
claude mcp add --transport http metricool https://ai.metricool.com/mcp
claude
```
בהפעלה הראשונה של Metricool ייפתח חלון התחברות: להתחבר עם Google (oraykin7@gmail.com).

## פתיחה בפעמים הבאות
```bash
cd ~/Documents/Projects/oraykin-media && git pull && claude
```
