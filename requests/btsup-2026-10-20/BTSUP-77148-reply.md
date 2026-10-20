# BTSUP-77148 — drafted reply (not posted)

Reporter: Gargi Purohit · Status: Biz Sys Review · 22 comments

**Context read from the full thread:** file size is not the cause. The image
failed to embed at 108KB, at 88KB and again at 40KB. The ticket title asks for
compression under 100KB, which is a misdiagnosis of the user's actual problem —
the image attaches instead of rendering inline in an Outreach template sent
through Gmail. Outreach support (Parm Atwal) asserted a changed Gmail security
setting and told her to come to internal IT, without naming the setting or
citing an article.

---

Hi @Gargi Purohit,

Short version: file size is not the problem here, so more compression will not
fix it. The image failed to embed at 108KB, at 88KB and again at 40KB — three
different sizes, same behaviour. We should stop chasing the file and look at
the rendering path.

On the Outreach support reply: that update came to you directly and was never
shared with us, so we have nothing on our side about a changed Gmail security
setting. I also can't act on it as written — it does not name the setting or
link an article, and "a security setting has changed in Gmail" covers a wide
surface. Before we start changing Google Workspace configuration on a
hypothesis, could you go back to Parm and ask for two specific things?

1. The exact Gmail or Google Workspace setting they believe is responsible.
2. The Outreach support article or documentation that describes this behaviour,
   so we can follow the same steps they are.

With either of those, I can check our Workspace configuration against it
directly and give you a definite answer.

In the meantime, two things that may unblock the send:

- **Host the image rather than embedding it.** Put the image somewhere
  accessible and reference it by URL in the template instead of uploading it.
  Hosted images render inline far more reliably than uploaded ones, and the
  file size stops mattering entirely.
- **Confirm the template renders in HTML, not plain text.** You mentioned you
  can't find the three-dots option in Outreach — that control lives in the Gmail
  compose window, not Outreach, and it is worth re-checking at the point you
  actually send.

Apologies this has run as long as it has. Once we have the specific setting or
the article from Outreach, I'll take it from there.

Mark
