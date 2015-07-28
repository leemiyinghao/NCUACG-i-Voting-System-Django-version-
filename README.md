# NCUACG i-Voting System

*Current Release: FUMITSUKI*
*This project release with WTFPL v2*

This is a work by NCUACG(http://ncuacg.pixnet.net) as a vote system.

It include a basic vote, and 'Video Vote', which check if user finish the video.
***
### Install & Config
- Download archive, extract it and `cd` in.
- Install twython

  ```bash
  pip install twython
  ```

- Add Twitter API Key & Secret into `NCUACG_ivot/setting`
- `./manage.py createsuperuser` to create an admin account to manage all the votes.
- Okay, now it's ready to depoly!

***

### Manage Guide
- Admin page is at `/admin/` by default. All action below must done in here.
  - Add new Vote in Vote List.
    - For a normal vote, select `selectVote`.
    - For a video vote that checking if user finish video, select `videoVote`.
    - Max selection will be only effective when vote type is `selectVote`.
    - Video length be effective when vote type is `videoVote`.
    - Video is play by HTML5 player, it's better to be an AVC1 MP4.
    - Add options for `selectVote`.
  - Add user into Voteable user list so they can vote.
  - Invoice by checking Vote record, and view Fetching record in Fetch vote record if you want.
    - Fetch vote record record every times user view the voteroom page.
    - If user vote for more than once, only the lastest vote will have their `mute = false`.

***

### Contact Us
- NCUACG Club Mailbox: ncuacg.tw@gmail.com

- i-Voting System Project Staff
  - catLee, Project Manager: leemiyinghao@gmx.com
  - cIII, Programer: jefferychen16@gmail.com
