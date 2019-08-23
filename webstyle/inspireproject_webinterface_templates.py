def tmpl_jobs_matrix(categories, ranks, counts):
    out = ["""<p>We are listing the number of job offers per field.</p>

<h4>"physics" refers to jobs that apply to any non-listed field.</h4>

<table cellpadding="4">
<tr>
<td></td>
<td>PhD</td>
<td>Postdoc</td>
<td>Junior</td>
<td>Senior</td>
<td>Staff</td>
<td>Visitor</td>
<td>Other</td>
</tr>"""]
    for cat in categories:
        out.append('<tr><td align="center">%s</td>' % cat)
        for rank in ranks:
            out.append("""
            <td align="center">
                <a href="https://labs.inspirehep.net/jobs?rank={0}&field_of_interest={1}">{2}</a>
            </td>
            """.format(rank, cat, counts[cat][rank]))
        out.append('</td></tr>')
    out.append("</table>")
    return ''.join(out)
