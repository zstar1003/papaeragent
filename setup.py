from setuptools import setup, find_packages

setup(
    name='academicagent',
    version='0.1.2',
    author='zstar',
    author_email='zstar1003@163.com',
    description='A package to download arXiv papers and interact with PDFs using Ollama LLM',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/zstar1003/papaeragent',  # 修改为你的项目主页
    packages=find_packages(),
    install_requires=[
        'requests',
        'lxml',
        'beautifulsoup4',
        'langchain_ollama',
        'langchain_community',
        'PyMuPDF',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)