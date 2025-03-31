'use client';
import { useState, useRef, useEffect } from 'react';

interface Message {
  sender: 'user' | 'bot';
  text: string;
  html?: boolean;
}

const TypingIndicator = ({ darkMode }: { darkMode: boolean }) => (
  <div className={`flex items-center gap-1 px-4 py-2 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'} w-fit`}>
    <div className={`w-2 h-2 rounded-full ${darkMode ? 'bg-gray-400' : 'bg-gray-500'} animate-bounce`} style={{ animationDelay: '0ms' }} />
    <div className={`w-2 h-2 rounded-full ${darkMode ? 'bg-gray-400' : 'bg-gray-500'} animate-bounce`} style={{ animationDelay: '150ms' }} />
    <div className={`w-2 h-2 rounded-full ${darkMode ? 'bg-gray-400' : 'bg-gray-500'} animate-bounce`} style={{ animationDelay: '300ms' }} />
  </div>
);

const MessageBubble = ({ message, darkMode }: { message: Message; darkMode: boolean }) => {
  const renderMarkdown = (text: string) => {
    return text
      .replace(/^# (.*$)/gm, `<h2 class="text-xl font-bold mt-4 mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}">$1</h2>`)
      .replace(/^## (.*$)/gm, `<h3 class="text-lg font-semibold mt-3 mb-1.5 ${darkMode ? 'text-gray-100' : 'text-gray-800'}">$1</h3>`)
      .replace(/^### (.*$)/gm, `<h4 class="font-medium mt-3 mb-1 ${darkMode ? 'text-gray-200' : 'text-gray-700'}">$1</h4>`)
      .replace(/\*\*(.*?)\*\*/g, `<strong class="font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}">$1</strong>`)
      .replace(/\*(.*?)\*/g, '<em class="italic">$1</em>')
      .replace(/`(.*?)`/g, `<code class="font-mono ${darkMode ? 'bg-gray-700 text-gray-100' : 'bg-gray-100 text-gray-800'} px-1 py-0.5 rounded">$1</code>`)
      .replace(/\n/g, '<br class="my-2" />');
  };

  return (
    <div className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-xl px-4 py-3 ${message.sender === 'user' 
          ? `${darkMode ? 'bg-blue-600' : 'bg-blue-600'} text-white rounded-br-none` 
          : `${darkMode ? 'bg-gray-700 text-gray-100' : 'bg-gray-100 text-gray-800'} rounded-bl-none`}`}
        dangerouslySetInnerHTML={{ __html: renderMarkdown(message.text) }}
      />
    </div>
  );
};

export default function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([
    { 
      sender: 'bot', 
      text: "Hello! I'm your xyz knowledge assistant. How can I help you today?\n\nYou can ask me things like:\n- **How to install softwarex**\n- **Softwarex configuration**\n- **Solution for SoftwareX configuration issues**"
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    setDarkMode(mediaQuery.matches);
    
    const handler = (e: MediaQueryListEvent) => setDarkMode(e.matches);
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await fetch('https://geminibotbe.onrender.com/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input })
      });

      if (!response.ok) throw new Error('Network response was not ok');
      
      const data = await response.json();
      const botMessage: Message = { sender: 'bot', text: data.response };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = { 
        sender: 'bot', 
        text: `Error: ${error instanceof Error ? error.message : 'Unknown error'}` 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className={`flex flex-col h-screen ${darkMode ? 'bg-gray-900 text-gray-100' : 'bg-gray-50 text-gray-900'}`}>
      {/* Header */}
      <header className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} shadow-sm py-4 px-6 border-b`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold`}>
              xyz
            </div>
            <div>
              <h1 className="font-bold text-lg">xyz Knowledge Assistant</h1>
              <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Powered by Gemini AI</p>
            </div>
          </div>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className={`p-2 rounded-full ${darkMode ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-200 hover:bg-gray-300'}`}
            aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {darkMode ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd" />
              </svg>
            )}
          </button>
        </div>
      </header>

      {/* Chat container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <MessageBubble key={index} message={message} darkMode={darkMode} />
        ))}
        {isTyping && (
          <div className="flex">
            <TypingIndicator darkMode={darkMode} />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <form 
        onSubmit={handleSubmit}
        className={`sticky bottom-0 ${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border-t p-4 shadow-sm`}
      >
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about xyz processes, guides, or solutions..."
            className={`flex-1 rounded-full ${darkMode ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' : 'border-gray-300'} border px-4 py-2 focus:outline-none focus:ring-2 ${darkMode ? 'focus:ring-blue-500' : 'focus:ring-blue-500'}`}
          />
          <button
            type="submit"
            disabled={!input.trim() || isTyping}
            className={`rounded-full bg-blue-600 text-white p-2 disabled:opacity-50 hover:bg-blue-700 transition-colors`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 1.414L10.586 9H7a1 1 0 100 2h3.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
        <p className={`text-xs mt-2 text-center ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
          Ask about installations, troubleshooting, or IT procedures
        </p>
      </form>
    </div>
  );
}
