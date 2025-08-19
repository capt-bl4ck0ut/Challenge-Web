export const metadata = {
  title: "Baby Next.js",
  description: "👶",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
