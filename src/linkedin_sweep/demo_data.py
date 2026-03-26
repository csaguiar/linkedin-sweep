from linkedin_sweep.models import CandidateItem


def seed_items() -> list[CandidateItem]:
    return [
        CandidateItem(
            author="Alicia Chen",
            text="We just shipped a lightweight retrieval benchmark for production LLM systems. Curious how others evaluate latency vs quality tradeoffs.",
            url="https://www.linkedin.com/feed/update/demo-1",
            suggested_action="comment",
            reason="Strong overlap with Cristiano's ML background; thoughtful technical comment would be high-signal.",
            score=0.92,
            draft_comment="Nice framing. The latency/quality tradeoff is where a lot of real-world pain hides — especially once retrieval quality variance starts dominating end-user experience.",
        ),
        CandidateItem(
            author="Toronto AI Builders",
            text="Meetup next week on applied AI in production. Speakers from local startups and research teams.",
            url="https://www.linkedin.com/feed/update/demo-2",
            suggested_action="like",
            reason="Relevant local network signal with low-effort engagement.",
            score=0.73,
        ),
        CandidateItem(
            author="Daniel Moreira",
            text="Excited to start a new role building recommendation systems in Canada!",
            url="https://www.linkedin.com/feed/update/demo-3",
            suggested_action="reply",
            reason="Warm network-style interaction; a short congratulatory reply is appropriate.",
            score=0.81,
            draft_comment="Congrats — very nice move. Recommendation systems in production are never boring. Wishing you a strong start.",
        ),
        CandidateItem(
            author="Generic Growth Guru",
            text="Comment \"AI\" and I’ll send you the top 100 prompts that changed my life.",
            url="https://www.linkedin.com/feed/update/demo-4",
            suggested_action="ignore",
            reason="Low-signal engagement bait.",
            score=0.08,
        ),
    ]
