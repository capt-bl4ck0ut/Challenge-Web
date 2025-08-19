'use client';

import { useState } from 'react';
import { getFlag } from './actions';

const IS_PROD = process.env.NODE_ENV === 'production';

export default function Home() {
  const [message, setMessage] = useState('');

  return (
    <>
      {message && <p>{message}</p>}
      <button
        onClick={async () => {
          if (IS_PROD) {
            setMessage('unavailable in production');
            return;
          }
          const { message } = await getFlag();
          setMessage(message);
        }}
      >
        give me the flag
      </button>
    </>
  );
}
