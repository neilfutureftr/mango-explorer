# # ⚠ Warning
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# [🥭 Mango Markets](https://mango.markets/) support is available at:
#   [Docs](https://docs.mango.markets/)
#   [Discord](https://discord.gg/67jySBhxrg)
#   [Twitter](https://twitter.com/mangomarkets)
#   [Github](https://github.com/blockworks-foundation)
#   [Email](mailto:hello@blockworks.foundation)

import typing

from solana.publickey import PublicKey

from .accountinfo import AccountInfo
from .context import Context
from .group import Group
from .lotsizeconverter import LotSizeConverter
from .market import Market, InventorySource
from .orderbookside import OrderBookSide
from .orders import Order
from .perpeventqueue import PerpEvent, PerpEventQueue
from .perpmarketdetails import PerpMarketDetails
from .token import Token


# # 🥭 PerpMarket class
#
# This class encapsulates our knowledge of a Mango perps market.
#
class PerpMarket(Market):
    def __init__(self, program_id: PublicKey, address: PublicKey, base: Token, quote: Token, underlying_perp_market: PerpMarketDetails):
        super().__init__(program_id, address, InventorySource.ACCOUNT, base, quote)
        self.underlying_perp_market: PerpMarketDetails = underlying_perp_market
        self.lot_size_converter: LotSizeConverter = LotSizeConverter(
            base, underlying_perp_market.base_lot_size, quote, underlying_perp_market.quote_lot_size)

    @property
    def symbol(self) -> str:
        return f"{self.base.symbol}-PERP"

    @property
    def group(self) -> Group:
        return self.underlying_perp_market.group

    def unprocessed_events(self, context: Context) -> typing.Sequence[PerpEvent]:
        event_queue: PerpEventQueue = PerpEventQueue.load(
            context, self.underlying_perp_market.event_queue, self.lot_size_converter)
        return event_queue.unprocessed_events

    def accounts_to_crank(self, context: Context, additional_account_to_crank: typing.Optional[PublicKey]) -> typing.Sequence[PublicKey]:
        accounts_to_crank: typing.List[PublicKey] = []
        for event_to_crank in self.unprocessed_events(context):
            accounts_to_crank += event_to_crank.accounts_to_crank

        if additional_account_to_crank is not None:
            accounts_to_crank += [additional_account_to_crank]

        seen = []
        distinct = []
        for account in accounts_to_crank:
            account_str = account.to_base58()
            if account_str not in seen:
                distinct += [account]
                seen += [account_str]
        distinct.sort(key=lambda address: address._key or [0])
        return distinct

    def orders(self, context: Context) -> typing.Sequence[Order]:
        bids_address: PublicKey = self.underlying_perp_market.bids
        asks_address: PublicKey = self.underlying_perp_market.asks
        [bids, asks] = AccountInfo.load_multiple(context, [bids_address, asks_address])
        bid_side = OrderBookSide.parse(context, bids, self.underlying_perp_market)
        ask_side = OrderBookSide.parse(context, asks, self.underlying_perp_market)
        return [*bid_side.orders(), *ask_side.orders()]

    def __str__(self) -> str:
        underlying: str = f"{self.underlying_perp_market}".replace("\n", "\n    ")
        return f"""« 𝙿𝚎𝚛𝚙𝙼𝚊𝚛𝚔𝚎𝚝 {self.symbol} {self.address} [{self.program_id}]
    {underlying}
»"""


# # 🥭 PerpMarketStub class
#
# This class holds information to load a `PerpMarket` object but doesn't automatically load it.
#
class PerpMarketStub(Market):
    def __init__(self, program_id: PublicKey, address: PublicKey, base: Token, quote: Token, group_address: PublicKey):
        super().__init__(program_id, address, InventorySource.ACCOUNT, base, quote)
        self.group_address: PublicKey = group_address

    def load(self, context: Context, group: typing.Optional[Group] = None) -> PerpMarket:
        actual_group: Group = group or Group.load(context, self.group_address)
        underlying_perp_market: PerpMarketDetails = PerpMarketDetails.load(context, self.address, actual_group)
        return PerpMarket(self.program_id, self.address, self.base, self.quote, underlying_perp_market)

    @property
    def symbol(self) -> str:
        return f"{self.base.symbol}-PERP"

    def __str__(self) -> str:
        return f"« 𝙿𝚎𝚛𝚙𝙼𝚊𝚛𝚔𝚎𝚝𝚂𝚝𝚞𝚋 {self.symbol} {self.address} [{self.program_id}] »"
