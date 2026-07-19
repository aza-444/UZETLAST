<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" 
                xmlns:html="http://www.w3.org/TR/REC-html40"
                xmlns:sitemap="http://www.sitemaps.org/schemas/sitemap/0.9"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml">
      <head>
        <title>XML Sitemap - UZEnergo Ta'minlash</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <style type="text/css">
          body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #333;
            margin: 0;
            padding: 40px;
            background-color: #0a0e1a; /* Dark theme background */
            background-image: radial-gradient(ellipse 60% 80% at 10% 50%, rgba(245,158,11,0.07) 0%, transparent 60%);
          }
          #content {
            max-width: 900px;
            margin: 0 auto;
            background: #111827;
            padding: 30px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.07);
            box-shadow: 0 4px 24px rgba(0,0,0,0.4);
          }
          h1 {
            font-size: 24px;
            color: #f1f5f9;
            margin-bottom: 10px;
          }
          p {
            font-size: 14px;
            color: #94a3b8;
            margin-bottom: 30px;
          }
          table {
            width: 100%;
            border-collapse: collapse;
          }
          th {
            text-align: left;
            padding: 14px;
            background-color: rgba(245, 158, 11, 0.1);
            font-size: 14px;
            color: #f59e0b;
            border-bottom: 2px solid rgba(255,255,255,0.1);
            text-transform: uppercase;
            letter-spacing: 0.5px;
          }
          td {
            padding: 14px;
            font-size: 14px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            color: #f1f5f9;
          }
          tr:hover td {
            background-color: rgba(255,255,255,0.02);
          }
          a {
            color: #3b82f6;
            text-decoration: none;
          }
          a:hover {
            color: #f59e0b;
            text-decoration: underline;
          }
          .back-link {
            display: inline-block;
            margin-bottom: 20px;
            color: #f59e0b;
            text-decoration: none;
            font-size: 14px;
            font-weight: 600;
          }
          .back-link:hover {
            text-decoration: underline;
          }
        </style>
      </head>
      <body>
        <div id="content">
          <a href="/" class="back-link">← Bosh sahifaga qaytish</a>
          <h1>XML Sitemap</h1>
          <p>Ushbu sitemap fayli qidiruv tizimlari (Google, Yandex) saytni tezroq va to'g'ri indekslashi uchun mo'ljallangan.</p>
          <table>
            <thead>
              <tr>
                <th>Sahifa havolasi (URL)</th>
                <th>Ustuvorlik (Priority)</th>
                <th>Yangilanish (Freq)</th>
              </tr>
            </thead>
            <tbody>
              <xsl:for-each select="sitemap:urlset/sitemap:url">
                <tr>
                  <td>
                    <xsl:variable name="itemURL">
                      <xsl:value-of select="sitemap:loc"/>
                    </xsl:variable>
                    <a href="{$itemURL}">
                      <xsl:value-of select="sitemap:loc"/>
                    </a>
                  </td>
                  <td>
                    <xsl:value-of select="sitemap:priority"/>
                  </td>
                  <td>
                    <xsl:value-of select="sitemap:changefreq"/>
                  </td>
                </tr>
              </xsl:for-each>
            </tbody>
          </table>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
