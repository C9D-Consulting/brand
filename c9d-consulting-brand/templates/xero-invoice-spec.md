# Xero invoice theme spec

**Status: PROPOSED.** An application of The Dossier to the client invoice, built as a Xero custom
.docx branding theme. Treat it as a starting point until reviewed in Xero's own preview.

Generator: `generators/c9d_xero_invoice_build.py`. Renders: `renders/xero-invoice/`. Build with
`make xero-invoice`.

## Why a custom .docx theme

Xero is the ledger of record and issues C9D Consulting invoices. Its standard branding themes
allow a logo and a few font and layout options, which cannot carry The Dossier. A custom .docx
theme can. Xero merges the theme with each invoice and sends the client a PDF, so the .docx is
an input to Xero, never something a client opens.

## Faces

Xero renders custom .docx themes itself and is reported to strip embedded fonts. The theme is
therefore set in faces every renderer carries:

| Brand face | Theme face | Used for |
| --- | --- | --- |
| Inter Tight | Arial | Body, headings, figures |
| JetBrains Mono | Courier New | Chrome, labels, invoice number, payment reference |

This is a recorded departure from the type stack, limited to this artifact. Colour, rules,
structure, the wordmark and the closing line are unchanged. If Xero is shown to honour the brand
faces, change `FACE` in the generator and rebuild.

## Layout

US Letter, 0.9in side margins, one page for a typical invoice. Light-mode tokens from
`assets/tokens.json`. Top to bottom:

1. Chrome row: `FILE` and the invoice number, `CLIENT CONFIDENTIAL` in stamp, `§ INVOICE`, hairline.
2. Masthead: the horizontal light wordmark (cropped to its ink and flattened onto white, because
   Xero rasterises images and mishandles transparency) and the title "Invoice".
3. Parties: Billed to, From, and the invoice facts (number, issued, due, reference).
4. Amount-due band: bg-2 fill with a stamp rule above, amount due in display size, due date and the
   payment-reference instruction. An accounts-payable reader sees what to pay and by when first.
5. Line items: repeating header row; description in ink bright with any second line of the Xero
   description in ink mute; quantity, rate and amount right-aligned.
6. Settlement: remittance details on the left (static, filled once in Word before upload), totals on
   the right with Amount due on the last row under a heavy rule. One table, so they stay together.
7. Terms: payment reference instruction, the CSA and SOW, the late charge "set out in that
   agreement" (the theme never restates a number the CSA governs).
8. Closing signature, then the attribution footer on every page.

## Merge fields

| Field | Where |
| --- | --- |
| `InvoiceNumber` | Chrome, facts, amount band, payment reference |
| `InvoiceDate`, `DueDate` | Facts and amount band, `\@ "MMM d, yyyy"` |
| `Reference` | Facts. Carries Engagement ID, SOW and the client PO |
| `ContactName`, `PostalAddress` | Billed to |
| `OrganisationName`, `OrganisationPostalAddress` | From |
| `TableStart:LineItem` ... `TableEnd:LineItem` | First and last cell of the one line-item row |
| `Description`, `Quantity`, `UnitAmount`, `LineAmount` | Line items, money as `\# "#,##0.00"` |
| `SubTotal`, `TaxTotal`, `Total`, `AmountPaid`, `AmountDue` | Totals |

`TableStart`, `TableEnd` and the line-item fields are confirmed by published Xero guidance.
`PostalAddress` and `TaxTotal` follow Xero's naming pattern but are not yet confirmed against
Xero's own starter template; check them first in Xero's preview. A wrong name prints blank.

Every field shows a sample value as its result, and the two table markers show nothing, so the
unmerged template reads like a finished invoice in Word and in phone previewers. Xero reads only
the field codes. When editing in Word, a field shades grey when selected and Alt+F9 shows the codes;
never type over a field.

## Robustness rules

- Every table declares a percentage width. Simple previewers autofit tables with a fixed or auto
  width down to their content.
- `tblInd` equals the left cell padding on filled or ruled tables, so fills sit on the margins.
- Paragraph and table properties are written in ECMA-376 order; the file passes OOXML validation.
- The stock `docDefaults` spacing (10pt after, 1.15 lines) is zeroed, or every unformatted cell
  paragraph inflates its row.

## Before upload

Fill the bracketed remittance placeholders (bank, routing numbers, account, billing email) in Word.
They are deliberately not in the generator, so no account details live in this repository. Then in
Xero: Settings, Invoice settings, New Branding Theme, Custom .docx, upload, and preview a draft
invoice before setting the theme as default.
