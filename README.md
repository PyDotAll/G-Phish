<div align="center">
  <img src="https://github.com/TranscriptAI/GPhish/assets/136038564/7b9530d2-3c30-4c1c-8f6c-ce4fec263ece" alt="MasterHead" width="50%">
</div>

<h1 align="center">GPhish</h1>
<p align="center">
  <a href="https://www.python.org">
    <img src="https://img.shields.io/badge/Python-3.11-blue.svg?logo=python" alt="Python" width="105"/>
  </a>
  <a href="https://bestpractices.coreinfrastructure.org/projects/7452">
    <img src="https://bestpractices.coreinfrastructure.org/projects/7452/badge" alt="OpenSSF Best Practices" width="242"/>
  </a>
  <a href="https://github.com/EthicalSource/contributor_covenant">
    <img src="https://img.shields.io/badge/code_of_conduct-contributor_covenant-14cc21?logo=github" alt="Code of Conduct: Contributor Covenant" width="254"/>
  </a>
  <a href="https://github.com/TranscriptAI/TranscribeAI/releases">
    <img src="https://img.shields.io/badge/version-1.0.0-blue.svg?logo=github" alt="Version" width="114"/>
  </a>
  <a href="https://ko-fi.com/R5R0M2YFE">
    <img src="https://img.shields.io/badge/sponsors-2-yellow.svg?logo=github" alt="Sponsors" width="99"/>
  </a>
  <a href="https://github.com/TranscriptAI/TranscribeAI/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/TranscriptAI/TranscribeAI.svg?logo=github" alt="Contributors" width="119"/>
  </a>
  <a href="https://github.com/TranscriptAI/TranscribeAI/discussions">
    <img src="https://img.shields.io/github/discussions/TranscriptAI/TranscribeAI.svg?logo=github" alt="Discussions" width="144"/>
  </a>
  <a href="https://github.com/TranscriptAI/TranscribeAI/issues">
    <img src="https://img.shields.io/github/issues/TranscriptAI/TranscribeAI.svg?logo=github" alt="Issues" width="114"/>
  </a>
  <a href="https://github.com/TranscriptAI/TranscribeAI/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License" width="83"/>
  </a>
</p>

## Overview
### Python, Javascript, HTML And CSS Integration 🥳
This repository contains the source code for creating a formal phishing attack in Gmail. The concept commonly relies on JQuery code injections somewhere in the HTML content of the sign-in page, using a minimal CDN in JS.

However, in spite of the possibility, there's no foolproof method for real hacking. The purpose of this repository is to provide a formal proof of concept for establishing a phishing attack in Gmail, for educational purposes only.
### Advantages Of GPhish 😏
> Code injection within '<script>' tag
>> Interaction between the attacker and the victim
>>> Easy to use with little to no setup
>>>> Based on Google's current CSS selectors 
### Disadvantages of GPhish 😒
> Runs on http but will soon be run on https
>> Does not support anonymity in account creation; use with precaution

Still fixing the checkbox that's triggering the malfunction. The fake_headers library only generates 50% success in achieving a 200 HTTP status code. I'm planning to create a workaround for this—maybe a good ML algorithm that can help it perform better.
## Installation
### Webdriver Manager Over The Regular 🥸
Please update your venv to 3.11 to avoid any further issues. If you don't have v3.11 yet, I highly encourage you to create one by installing the necessary Python version for it. This would make the code execution more robust.

Please make sure to pip install a webdriver manager in your venv to automatically manage drivers for different browsers. This ensures the compatibility of the Selenium web driver, making the executable file size larger than usual. In Windows, the file is automatically stored in _"C:\Users\Username\.wdm"_ directory.
```cmd
(venv_name) C:\Users\Username\python_project_file>pip install webdriver-manager
```
After pip installing webdriver-manager, install undetectable-chromedriver using this command:
```cmd
(venv_name) C:\Users\Username\python_project_file>pip install undetectable-chromedriver
```
The purpose of using this is to optimize the Selenium Chromedriver patch. This avoids the triggering of anti-bot services like Distill Network, Imperva, DataDome, Botprotect.io, and so on. This also automatically downloads the driver binary and patches it.
### Don't Forget Selenium 😇
However, don't be confused about what's called a webdriver or webdriver-manager. Therefore, you should still install Selenium via pip because it's the most crucial part of making browser automation possible at POC.py.
```cmd
(venv_name) C:\Users\Username\python_project_file>pip install -U selenium
```
### Other Non-Default Installations 😄
For other non-default python libraries, please install via main/requirements.txt. Most of them are only HTML parsers that need to be installed to improve the deliverability of HTML parsing and encoding detection using bs4 library.
## Usage
### Just Run POC.py 🤩
That's how simple it is. If you have any concerns on your own end or any enhancements, please do let me know. You can convert POC.py to executable file using pyinstaller library if you want a simple click, but that would require modifications to the code to integrate CLI using Windows' CMD.
### Gmail Sample Page 😚
Here's the gmail sample phishing page:
![Screenshot 2023-07-07 182949](https://github.com/TranscriptAI/GPhish/assets/136038564/e4f2afef-6171-4d4a-b2be-ff5bf4e4d7e1)
## Sponsors
Support this project by becoming a sponsor! Your sponsorship helps to maintain and improve this project and soon be able to develop a playground for pentesters and infosec experts who are willing and interested.
## Contributors
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature/fix:
```shell
git checkout -b feature/your-feature-name
```
3. Make your changes and test thoroughly.
4. Commit your changes:
```shell
git commit -m "Add your commit message here"
```
5. Push to the branch:
```shell
git push origin feature/your-feature-name
```
6. Open a pull request, describing your changes in detail.
## Discussions
To join the discussions, ask questions, share ideas, and get support, follow these steps:
1. To find the general discussion thread where you will add a comment, click [here](https://github.com/TranscriptAI/TranscribeAI/discussions/1).
2. Inside the discussion thread, scroll down to view the existing comments and find the comment box.
3. In the comment box, type your comment or response to the discussion. format your comment using Markdown, allowing you to add formatting and more.
4. To preview how your comment will look before posting it, click the **Preview** tab located below the comment box to help ensure your comment appears as intended.
5. After you've written your comment and reviewed it, click the **Comment** or **Submit** button to add your comment to the discussion thread.
To receive notifications about new comments or updates to the discussion, click the **Watch** button near the top-right corner of the discussion page. This will ensure you stay up to date with any new activity in the discussion. And that's it! Your comment should now be added to the GitHub discussion thread.
## Issues
To use issue tracker for bug reports, custom feature requests, and other issues, follow these steps:
1. Click [here](https://github.com/TranscriptAI/TranscribeAI/issues/new/choose) to create new issue.
2. In the issue creation form, enter a title for your issue. Also in the main text area, provide a detailed description of the issue, including any relevant information such as steps to reproduce a bug or suggestions for implementing a new feature.
3. To add labels, click the **Labels** button on the right-hand side of the issue form. To assign an issue, click the **Assignees** button.
4. Add additional context by attaching files, including screenshots or code snippets, by clicking on the **Attach files** button. Use the formatting options provided by Markdown to structure your issue description or add code blocks.
5. If you want to see how your issue will look before submitting it, click the **Preview** tab located below the issue form. This step is optional but can help ensure your issue appears as intended.
6. After you've provided all the necessary information, click the **Submit new issue** button at the bottom of the form to create the issue. That's it! You've successfully created an issue on GitHub.
## License
This software is licensed under the **MIT License**.
