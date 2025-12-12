import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { useAuth } from '../../../contexts/AuthContext';
import OriginalContent from '@theme-original/DocItem/Content';

function PersonalizedContent(props) {
  const { user } = useAuth();
  const [personalizedContent, setPersonalizedContent] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handlePersonalize = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/personalize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          content: props.children.props.children, 
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to personalize content');
      }

      const data = await response.json();
      setPersonalizedContent(data.personalized_content);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      {user && (
        <button onClick={handlePersonalize} disabled={isLoading} style={{marginBottom: "1rem"}}>
          {isLoading ? 'Personalizing...' : '✨ Personalize This Chapter'}
        </button>
      )}
      {personalizedContent ? (
        <div dangerouslySetInnerHTML={{ __html: personalizedContent }} />
      ) : (
        <OriginalContent {...props} />
      )}
    </div>
  );
}


export default function Content(props) {
  return (
    <BrowserOnly fallback={<OriginalContent {...props} />}>
      {() => <PersonalizedContent {...props} />}
    </BrowserOnly>
  );
}