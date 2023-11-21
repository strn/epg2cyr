<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="text" encoding="utf-8"/>
    <xsl:strip-space elements="*" />

    <xsl:variable name="newline" select="'&#10;'" />
    <xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyz'" />
    <xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'" />

    <xsl:template match="/tv">
        <xsl:for-each select="//channel">
            <xsl:value-of select="translate(@id, $uppercase, $lowercase)" />
            <xsl:text>|</xsl:text>
            <xsl:value-of select="display-name" />
            <xsl:value-of select="$newline" />
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>
