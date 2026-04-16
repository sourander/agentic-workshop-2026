FROM --platform=linux/amd64 mattermost/mattermost-team-edition:latest AS base

FROM --platform=linux/amd64 alpine:latest AS modifier
COPY --from=base /mattermost /mattermost
RUN chgrp -R 0 /mattermost && chmod -R g=u /mattermost

FROM base
COPY --from=modifier /mattermost /mattermost
USER 2000
