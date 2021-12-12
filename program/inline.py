from pyrogram import Client, errors
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from youtubesearchpython import VideosSearch


@Client.on_inline_query()
async def inline(client: Client, query: InlineQuery):
    answers = []
    search_query = query.query.lower().strip().rstrip()

    if search_query == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text="ᴛʏᴘᴇ ᴀ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ ɴᴀᴍᴇ...",
            switch_pm_parameter="help",
            cache_time=0,
        )
    else:
        search = VideosSearch(search_query, limit=50)

        for result in search.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=result["title"],
                    description="{}, {} views.".format(
                        result["duration"], result["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "🔗 https://www.youtube.com/watch?v={}".format(result["id"])
                    ),
                    thumb_url=result["thumbnails"][0]["url"],
                )
            )

        try:
            await query.answer(results=answers, cache_time=0)
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="error: ꜱᴇᴀʀᴄʜ ᴛɪᴍᴇᴅ ᴏᴜᴛ",
                switch_pm_parameter="",
            )
