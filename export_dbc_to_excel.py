def write_message_table(ws, message, start_row):
    headers = [
        "Signal Name", "Start Bit", "Length (bits)", "Byte Order", "Signed",
        "Factor", "Offset", "Min", "Max", "Unit", "Choices"
    ]
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=start_row, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border

    row_index = start_row + 1

    if not message.signals:
        # Write a row saying "No signals"
        cell = ws.cell(row=row_index, column=1, value="(No signals defined in this message)")
        cell.font = Font(italic=True)
        row_index += 1
    else:
        for sig in message.signals:
            try:
                unit = sig.unit.encode("utf-8", errors="replace").decode("utf-8") if sig.unit else ""
                choices = ", ".join(f"{k}={v}" for k, v in sig.choices.items()) if sig.choices else ""

                row_data = [
                    sig.name,
                    sig.start,
                    sig.length,
                    "Intel" if sig.byte_order == "little_endian" else "Motorola",
                    sig.is_signed,
                    sig.scale,
                    sig.offset,
                    sig.minimum,
                    sig.maximum,
                    unit,
                    choices
                ]

                for col_index, value in enumerate(row_data, start=1):
                    cell = ws.cell(row=row_index, column=col_index, value=value)
                    cell.border = thin_border

                row_index += 1
            except Exception as e:
                print(f"⚠️ Skipped signal '{getattr(sig, 'name', 'UNKNOWN')}' in message '{message.name}' due to error: {e}")

    return row_index + 1  # add blank row after
