/**
 * TranslateButton - Placeholder component for Urdu translation feature
 *
 * TODO: Future implementation should:
 * - Integrate with translation API (Google Translate, DeepL, or custom model)
 * - Store translations in cache to avoid repeated API calls
 * - Maintain markdown structure and code blocks during translation
 * - Support bidirectional text rendering (RTL for Urdu)
 * - Allow toggling between English and Urdu with smooth transitions
 * - Preserve technical terms in English (e.g., "Physical AI", "ROS 2")
 * - Translate UI elements (sidebar, buttons, labels)
 *
 * Phase 2 Implementation Requirements:
 * - Translation API integration (backend service)
 * - Caching layer for translated content (Redis or PostgreSQL)
 * - RTL layout support in CSS
 * - Language preference storage (localStorage)
 * - Fallback to English for untranslated sections
 * - Quality assurance for technical accuracy
 */
import React, { useState } from 'react';
import { useHistory } from '@docusaurus/router';

export default function TranslateButton(): JSX.Element {
  const [isLoading, setIsLoading] = useState(false);
  const [isTranslated, setIsTranslated] = useState(false);
  const [originalContent, setOriginalContent] = useState('');
  const history = useHistory();

  const handleTranslate = async () => {
    // 1. Check for auth token
    const token = localStorage.getItem('auth_token');
    if (!token) {
      history.push('/signin');
      return;
    }

    const chapterContentElement = document.getElementById('chapter-content');
    if (!chapterContentElement) {
      console.error('Chapter content container not found.');
      return;
    }

    setIsLoading(true);

    // Toggle back to English if already translated
    if (isTranslated) {
      chapterContentElement.innerHTML = originalContent;
      setIsTranslated(false);
      setIsLoading(false);
      return;
    }

    try {
      // 2. Capture content
      const contentToTranslate = chapterContentElement.innerHTML;
      setOriginalContent(contentToTranslate);

      // 3. Send to backend
      const response = await fetch('/api/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ content: contentToTranslate, target_language: 'Urdu' }),
      });

      if (!response.ok) {
        throw new Error(`Translation API failed with status: ${response.status}`);
      }

      const data = await response.json();

      // 4. Replace content with translation
      if (data.translated_text) {
        chapterContentElement.innerHTML = data.translated_text;
        setIsTranslated(true);
      }
    } catch (error) {
      console.error('Translation failed:', error);
      alert('An error occurred during translation. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      className="translate-button"
      onClick={handleTranslate}
      disabled={isLoading}
      aria-label={isTranslated ? "Show original English content" : "Translate chapter to Urdu"}
      title={isTranslated ? "Show original English content" : "Translate this chapter to Urdu"}
    >
      {isLoading ? (
        <span className="translate-label">Translating...</span>
      ) : (
        <>
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="translate-icon"
          >
            <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" />
            <path d="M2 12h20" stroke="currentColor" strokeWidth="2" />
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" stroke="currentColor" strokeWidth="2" />
          </svg>
          <span className="translate-text">{isTranslated ? 'English' : 'اردو'}</span>
          <span className="translate-label">{isTranslated ? 'English' : 'Urdu'}</span>
        </>
      )}
    </button>
  );
}
